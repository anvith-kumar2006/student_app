from flask import Flask, render_template, request, redirect, session, flash, Response
import mysql.connector
import random, string
import pandas as pd
import csv
from io import StringIO

app = Flask(__name__)
app.secret_key = "secret123"

db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="admin",
    database="student_db",
    autocommit=True
)
cursor = db.cursor(buffered=True)


def generate_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


# ================= AI RISK FUNCTION =================
def calculate_risk(internal, assignment, attendance, min_internal, min_assignment, min_attendance):

    internal = internal or 0
    assignment = assignment or 0
    attendance = attendance or 0

    min_internal = min_internal or 0
    min_assignment = min_assignment or 0
    min_attendance = min_attendance or 0

    if internal < min_internal or assignment < min_assignment or attendance < min_attendance:
        return "At-Risk"

    elif (
        internal < (1.2 * min_internal) or
        assignment < (1.2 * min_assignment) or
        attendance < (1.2 * min_attendance)
    ):
        return "Warning"

    else:
        return "Good"


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if request.form['password'] != request.form['confirm_password']:
            return "Passwords do not match"

        email = request.form['email'].lower()

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            return "Email already exists"

        try:
            cursor.execute(
                "INSERT INTO users (name,email,role,password) VALUES (%s,%s,%s,%s)",
                (request.form['name'], email, request.form['role'], request.form['password'])
            )
            db.commit()
        except Exception as e:
            print("REGISTER ERROR:", e)
            return "Error occurred while registering"

        return redirect('/login')

    return render_template('register.html')


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':

        if not db.is_connected():
            db.reconnect()

        cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (request.form['email'], request.form['password'])
        )
        user = cursor.fetchone()

        if user:
            session['user_id'] = user[0]
            session['name'] = user[1]
            session['email'] = user[2]
            session['role'] = user[3]

            if user[3] == 'student':
                return redirect('/student')
            else:
                return redirect('/teacher')

        return "Invalid credentials"

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/student')
def student():
    if not db.is_connected():
        db.reconnect()

    if 'user_id' not in session or session.get('role') != 'student':
        return redirect('/login')

    user_id = session['user_id']

    cursor.execute("""
        SELECT DISTINCT c.class_name, c.class_code
        FROM student_subjects ss
        JOIN subjects sub ON ss.subject_id = sub.id
        JOIN classrooms c ON sub.class_id = c.id
        WHERE ss.student_id = %s
    """, (user_id,))
    classes = cursor.fetchall()

    cursor.execute("""
        SELECT COUNT(DISTINCT subject_id)
        FROM student_subjects
        WHERE student_id = %s
    """, (user_id,))
    subject_count = cursor.fetchone()[0]

    cursor.execute("""
        SELECT sub.subject_name, 
               m.internal_marks,
               m.assignment_marks,
               m.attendance,
               m.total_marks,
               sub.min_internal_marks,
               sub.assignment_marks,
               sub.min_attendance
        FROM marks m
        JOIN subjects sub ON m.subject_id = sub.id
        WHERE m.student_id = %s
    """, (user_id,))

    data = cursor.fetchall()

    marks = []
    subjects = []
    totals = []

    for m in data:
        subject, internal, assignment, attendance, total, min_i, min_a, min_att = m

        total = min(100, total or 0)
        risk = calculate_risk(internal, assignment, attendance, min_i, min_a, min_att)

        # ✅ FIXED BACKLOG LOGIC
        if risk == "At-Risk":
            backlog = "High"
        elif risk == "Warning":
            backlog = "Medium"
        else:
            backlog = "Low"

        if attendance < min_att:
            suggestion = "Improve attendance"
        elif internal < min_i:
            suggestion = "Focus on internal exams"
        elif assignment < min_a:
            suggestion = "Submit assignments properly"
        else:
            suggestion = "Keep performing well"

        marks.append((subject, internal or 0, assignment or 0, attendance or 0, total, risk, backlog, suggestion))
        subjects.append(subject)
        totals.append(total)

    return render_template(
        'student_dashboard.html',
        classes=classes,
        subject_count=subject_count,
        marks=marks,
        subjects=subjects,
        totals=totals
    )


@app.route('/teacher')
def teacher():

    if not db.is_connected():
        db.reconnect()

    if 'user_id' not in session or session.get('role') != 'teacher':
        return redirect('/login')

    teacher_id = session['user_id']

    cursor.execute("SELECT id, class_name FROM classrooms WHERE teacher_id=%s", (teacher_id,))
    classes = cursor.fetchall()

    cursor.execute("""
        SELECT DISTINCT u.id, u.name, u.email,
               COALESCE(c.class_name, c2.class_name) AS class_name
        FROM users u
        LEFT JOIN students s ON u.id = s.user_id
        LEFT JOIN classrooms c ON s.class_id = c.id
        LEFT JOIN student_subjects ss ON u.id = ss.student_id
        LEFT JOIN subjects sub ON ss.subject_id = sub.id
        LEFT JOIN classrooms c2 ON sub.class_id = c2.id
        WHERE u.role = 'student'
        AND (c.teacher_id = %s OR c2.teacher_id = %s)
    """, (teacher_id, teacher_id))
    students = cursor.fetchall()

    cursor.execute("""
        SELECT id, subject_name FROM subjects
        WHERE class_id IN (
            SELECT id FROM classrooms WHERE teacher_id = %s
        )
    """, (teacher_id,))
    subjects = cursor.fetchall()

    cursor.execute("""
        SELECT sub.subject_name, AVG(m.total_marks)
        FROM marks m
        JOIN subjects sub ON m.subject_id = sub.id
        JOIN classrooms c ON sub.class_id = c.id
        WHERE c.teacher_id = %s
        GROUP BY sub.subject_name
    """, (teacher_id,))
    graph_data = cursor.fetchall()

    graph_subjects = [g[0] for g in graph_data] if graph_data else []
    graph_avg = [min(100, float(g[1])) for g in graph_data] if graph_data else []

    cursor.execute("""
        SELECT u.name, AVG(m.total_marks)
        FROM marks m
        JOIN users u ON m.student_id = u.id
        JOIN subjects sub ON m.subject_id = sub.id
        JOIN classrooms c ON sub.class_id = c.id
        WHERE c.teacher_id = %s
        GROUP BY u.name
    """, (teacher_id,))
    student_graph = cursor.fetchall()

    student_names = [s[0] for s in student_graph] if student_graph else []
    student_avg = [min(100, float(s[1])) for s in student_graph] if student_graph else []

    weak_subject = min(graph_data, key=lambda x: x[1])[0] if graph_data else None
    top_student = max(student_graph, key=lambda x: x[1])[0] if student_graph else None

    cursor.execute("""
        SELECT u.name, sub.subject_name, m.internal_marks, m.assignment_marks, m.attendance,
        sub.min_internal_marks, sub.assignment_marks, sub.min_attendance
        FROM marks m
        JOIN users u ON m.student_id = u.id
        JOIN subjects sub ON m.subject_id = sub.id
        JOIN classrooms c ON sub.class_id = c.id
        WHERE c.teacher_id = %s
    """, (teacher_id,))

    risk_data = cursor.fetchall()
    risky_students = []

    for r in risk_data:
        name, subject, internal, assignment, attendance, min_i, min_a, min_att = r
        risk = calculate_risk(internal, assignment, attendance, min_i, min_a, min_att)

        if risk == "At-Risk":
            risky_students.append((name, subject, internal or 0, attendance or 0))

    return render_template(
        'teacher_dashboard.html',
        classes=classes,
        students=students,
        subjects=subjects,
        graph_subjects=graph_subjects,
        graph_avg=graph_avg,
        student_names=student_names,
        student_avg=student_avg,
        risky_students=risky_students,
        weak_subject=weak_subject,
        top_student=top_student
    )


@app.route('/add_marks', methods=['POST'])
def add_marks():
    student_id = request.form['student_id']
    subject_id = request.form['subject_id']
    marks = int(request.form['marks'])

    internal = min(50, marks)
    assignment = min(50, marks)
    attendance = 75

    total = min(100, internal + assignment)

    cursor.execute("""
        INSERT INTO marks (student_id, subject_id, internal_marks, assignment_marks, attendance, total_marks)
        VALUES (%s,%s,%s,%s,%s,%s)
        ON DUPLICATE KEY UPDATE
        internal_marks=%s, assignment_marks=%s, attendance=%s, total_marks=%s
    """, (
        student_id, subject_id, internal, assignment, attendance, total,
        internal, assignment, attendance, total
    ))

    db.commit()
    return redirect('/teacher')


@app.route('/create_class', methods=['POST'])
def create_class():
    code = generate_code()
    cursor.execute(
        "INSERT INTO classrooms (class_name,class_code,teacher_id) VALUES (%s,%s,%s)",
        (request.form['class_name'], code, session['user_id'])
    )
    db.commit()
    flash(f"Class Code: {code}")
    return redirect('/teacher')


@app.route('/add_subject', methods=['POST'])
def add_subject():
    code = generate_code(5)

    cursor.execute("""
        INSERT INTO subjects (subject_name,subject_code,class_id,min_attendance,min_internal_marks,assignment_marks)
        VALUES (%s,%s,%s,%s,%s,%s)
    """, (
        request.form['subject_name'],
        code,
        int(request.form['class_id']),
        request.form['min_attendance'],
        request.form['min_marks'],
        request.form['assignment_marks']
    ))

    db.commit()
    flash(f"Subject Code: {code}")
    return redirect('/teacher')


@app.route('/join_class', methods=['POST'])
def join_class():
    cursor.execute("SELECT id FROM classrooms WHERE class_code=%s", (request.form['class_code'],))
    c = cursor.fetchone()

    if not c:
        return "Invalid code"

    class_id = c[0]

    try:
        cursor.execute(
            "INSERT INTO students (user_id,class_id) VALUES (%s,%s)",
            (session['user_id'], class_id)
        )
        db.commit()
    except:
        return redirect('/student')

    cursor.execute("SELECT id FROM subjects WHERE class_id=%s", (class_id,))
    subjects = cursor.fetchall()

    for sub in subjects:
        cursor.execute("""
            INSERT IGNORE INTO student_subjects (student_id, subject_id)
            VALUES (%s,%s)
        """, (session['user_id'], sub[0]))

    db.commit()
    return redirect('/student')


@app.route('/upload_marks', methods=['POST'])
def upload_marks():
    file = request.files['file']
    subject_id = request.form['subject_id']

    if not file:
        return "No file uploaded"

    df = pd.read_csv(file) if file.filename.endswith('.csv') else pd.read_excel(file)

    for _, row in df.iterrows():
        try:
            email = row['email']

            internal = min(50, int(row['internal_marks']))
            assignment = min(50, int(row['assignment_marks']))
            attendance = min(100, int(row['attendance']))

            total = min(100, internal + assignment)

            cursor.execute("SELECT id FROM users WHERE email=%s", (email,))
            student = cursor.fetchone()

            if student:
                student_id = student[0]

                cursor.execute("""
                    INSERT IGNORE INTO student_subjects (student_id, subject_id)
                    VALUES (%s,%s)
                """, (student_id, subject_id))

                cursor.execute("""
                    INSERT INTO marks 
                    (student_id, subject_id, internal_marks, assignment_marks, attendance, total_marks)
                    VALUES (%s,%s,%s,%s,%s,%s)
                    ON DUPLICATE KEY UPDATE
                    internal_marks=%s, assignment_marks=%s, attendance=%s, total_marks=%s
                """, (student_id, subject_id, internal, assignment, attendance, total,
                      internal, assignment, attendance, total))

        except:
            continue

    db.commit()
    return redirect('/teacher')


@app.route('/download_report')
def download_report():
    if 'user_id' not in session or session.get('role') != 'student':
        return redirect('/login')

    user_id = session['user_id']

    cursor.execute("""
        SELECT sub.subject_name, 
               m.internal_marks,
               m.assignment_marks,
               m.attendance,
               m.total_marks
        FROM marks m
        JOIN subjects sub ON m.subject_id = sub.id
        WHERE m.student_id = %s
    """, (user_id,))

    data = cursor.fetchall()

    output = StringIO()
    writer = csv.writer(output)

    writer.writerow(["Subject", "Internal", "Assignment", "Attendance", "Total"])

    for row in data:
        writer.writerow(row)

    output.seek(0)

    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=student_report.csv"}
    )


if __name__ == "__main__":
    app.run(debug=True)