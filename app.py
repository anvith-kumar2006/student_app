from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# ✅ MySQL Connection (UPDATED AS YOU REQUESTED)
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="admin",
    database="student_db",
    port=3306,
    auth_plugin='mysql_native_password'
)

cursor = db.cursor()


# 🏠 HOME PAGE
@app.route('/')
def home():
    return render_template('home.html')


# 📝 REGISTER PAGE
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        role = request.form['role']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Password check
        if password != confirm_password:
            return "❌ Passwords do not match"

        # Insert into DB
        query = "INSERT INTO users (name, email, role, password) VALUES (%s, %s, %s, %s)"
        values = (name, email, role, password)

        cursor.execute(query, values)
        db.commit()

        return redirect(url_for('login'))

    return render_template('register.html')


# 🔐 LOGIN PAGE
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        query = "SELECT * FROM users WHERE email=%s AND password=%s"
        cursor.execute(query, (email, password))

        user = cursor.fetchone()

        if user:
            role = user[3]  # role column

            if role == 'student':
                return redirect(url_for('student_dashboard'))
            elif role == 'teacher':
                return redirect(url_for('teacher_dashboard'))
        else:
            return "❌ Invalid Email or Password"

    return render_template('login.html')


# 👨‍🎓 STUDENT DASHBOARD
@app.route('/student')
def student_dashboard():
    return render_template('student_dashboard.html')


# 👨‍🏫 TEACHER DASHBOARD
@app.route('/teacher')
def teacher_dashboard():
    return render_template('teacher_dashboard.html')


# ▶️ RUN APP
if __name__ == '__main__':
    app.run(debug=True)