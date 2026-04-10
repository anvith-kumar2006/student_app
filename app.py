from flask import Flask, render_template, request, redirect, session, flash
import mysql.connector
import random, string

app = Flask(__name__)
app.secret_key = "secret123"

db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="admin",
    database="student_db"
)
cursor = db.cursor()

def generate_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# HOME
@app.route('/')
def home():
    return render_template('home.html')

# REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if request.form['password'] != request.form['confirm_password']:
            return "Passwords do not match"

        try:
            cursor.execute(
                "INSERT INTO users (name,email,role,password) VALUES (%s,%s,%s,%s)",
                (request.form['name'], request.form['email'], request.form['role'], request.form['password'])
            )
            db.commit()
        except:
            return "Email already exists"

        return redirect('/login')

    return render_template('register.html')

# LOGIN
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (request.form['email'], request.form['password'])
        )
        user = cursor.fetchone()

        if user:
            session['user_id'] = user[0]
            session['role'] = user[3]
            return redirect('/student' if user[3]=='student' else '/teacher')

        return "Invalid credentials"

    return render_template('login.html')

# LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# ================= TEACHER DASHBOARD =================
@app.route('/teacher')
def teacher():
    if 'user_id' not in session:
        return redirect('/login')

    teacher_id = session['user_id']

    # Classes
    cursor.execute("SELECT id, class_name FROM classrooms WHERE teacher_id=%s", (teacher_id,))
    classes = cursor.fetchall()

    # Students (FIXED IDs)
    cursor.execute("""
    SELECT s.user_id, u.name, u.email, c.class_name
    FROM students s
    JOIN users u ON s.user_id = u.id
    JOIN classrooms c ON s.class_id = c.id
    WHERE c.teacher_id = %s
    """, (teacher_id,))
    students = cursor.fetchall()

    # 🔥 Subjects (IMPORTANT FIX)
    cursor.execute("""
    SELECT id, subject_name FROM subjects
    WHERE class_id IN (
        SELECT id FROM classrooms WHERE teacher_id = %s
    )
    """, (teacher_id,))
    subjects = cursor.fetchall()

    return render_template(
        'teacher_dashboard.html',
        classes=classes,
        students=students,
        subjects=subjects   # 🔥 REQUIRED
    )

# ================= STUDENT DASHBOARD =================
@app.route('/student')
def student():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']

    # Classes
    cursor.execute("""
        SELECT c.class_name, c.class_code
        FROM students s
        JOIN classrooms c ON s.class_id = c.id
        WHERE s.user_id = %s
    """, (user_id,))
    classes = cursor.fetchall()

    # Subject count
    cursor.execute("""
        SELECT COUNT(*)
        FROM subjects sub
        JOIN students s ON sub.class_id = s.class_id
        WHERE s.user_id = %s
    """, (user_id,))
    subject_count = cursor.fetchone()[0]

    # Marks
    cursor.execute("""
        SELECT sub.subject_name, m.marks
        FROM marks m
        JOIN subjects sub ON m.subject_id = sub.id
        WHERE m.student_id = %s
    """, (user_id,))
    marks = cursor.fetchall()

    return render_template(
        'student_dashboard.html',
        classes=classes,
        subject_count=subject_count,
        marks=marks
    )

# ================= CREATE CLASS =================
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

# ================= ADD SUBJECT =================
@app.route('/add_subject', methods=['POST'])
def add_subject():
    code = generate_code(5)

    cursor.execute("""
    INSERT INTO subjects (subject_name,subject_code,class_id,min_attendance,min_internal_marks,assignment_marks)
    VALUES (%s,%s,%s,%s,%s,%s)
    """,(
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

# ================= JOIN CLASS =================
@app.route('/join_class', methods=['POST'])
def join_class():
    cursor.execute("SELECT id FROM classrooms WHERE class_code=%s", (request.form['class_code'],))
    c = cursor.fetchone()

    if not c:
        return "Invalid code"

    class_id = c[0]

    # Prevent duplicate join
    try:
        cursor.execute(
            "INSERT INTO students (user_id,class_id) VALUES (%s,%s)",
            (session['user_id'], class_id)
        )
        db.commit()
    except:
        return redirect('/student')

    # Assign subjects automatically
    cursor.execute("SELECT id FROM subjects WHERE class_id=%s", (class_id,))
    subjects = cursor.fetchall()

    for sub in subjects:
        cursor.execute("""
            INSERT IGNORE INTO student_subjects (student_id, subject_id)
            VALUES (%s,%s)
        """, (session['user_id'], sub[0]))

    db.commit()

    return redirect('/student')

# ================= ADD MARKS =================
@app.route('/add_marks', methods=['POST'])
def add_marks():
    student_id = request.form['student_id']
    subject_id = request.form['subject_id']
    marks = request.form['marks']

    cursor.execute("""
        INSERT INTO marks (student_id, subject_id, marks)
        VALUES (%s,%s,%s)
    """, (student_id, subject_id, marks))

    db.commit()
    return redirect('/teacher')

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)