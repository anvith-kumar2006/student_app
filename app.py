from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# 🔹 MySQL Connection (FIXED VERSION)
try:
    db = mysql.connector.connect(
        host="127.0.0.1",   # IMPORTANT
        user="root",
        password="admin",
        database="student_db",
        port=3306,
        auth_plugin='mysql_native_password'
    )
    cursor = db.cursor()
    print("✅ MySQL Connected Successfully")

except mysql.connector.Error as err:
    print(f"❌ Connection Error: {err}")


# 🔹 Home Page
@app.route('/')
def home():
    return render_template("index.html")


# 🔹 Prediction + Store Data
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # 🔹 Get form data
        name = request.form['name']
        attendance = int(request.form['attendance'])
        marks = int(request.form['marks'])
        cgpa = float(request.form['cgpa'])

        print("📥 Received:", name, attendance, marks, cgpa)

        # 🔹 Logic
        if attendance < 75 and marks < 40:
            result = "High Risk"
            color = "red"
        elif cgpa < 6:
            result = "Medium Risk"
            color = "orange"
        else:
            result = "Low Risk"
            color = "green"

        print("📊 Result:", result)

        # 🔹 Insert into DB
        try:
            query = """
            INSERT INTO students (name, attendance, marks, cgpa, result)
            VALUES (%s, %s, %s, %s, %s)
            """
            values = (name, attendance, marks, cgpa, result)

            cursor.execute(query, values)
            db.commit()

            print("✅ Data inserted successfully")

        except Exception as e:
            print("❌ Insert Error:", e)

        # 🔹 Show result
        return render_template("result.html", name=name, result=result, color=color)

    except Exception as e:
        return f"❌ Error: {e}"


# 🔹 Run App
if __name__ == '__main__':
    app.run(debug=True)