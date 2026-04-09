# student_app
AI-Based Student Performance Analysis and Backlog Risk Prediction System

Problem statement:

In many educational  institutions, identifying  backlogs is a challenging task. Traditional evaluation methods rely heavily on final exam results, which do not provide early warnings or insights into a student’s progress throughout the semester.
Factors such as low attendance, poor internal assessment scores, insufficient study hours, and previous academic history significantly influence a student’s performance. However, these factors are often not analyzed collectively in a systematic and data-driven manner.
This project aims to develop a system that analyzes student data using computational techniques to predict academic performance and assess the risk of backlogs in advance. By leveraging parameters such as attendance, internal marks, study habits, CGPA, and backlog history, the system provides early predictions and actionable insights.
The goal is to assist educators and institutions in identifying at-risk students at an early stage, enabling timely interventions, personalized support, and improved academic outcomes.

project team :
Anvith kumar,
Kachithananadha,
Harishkumar.


🧠 1. SYSTEM DESIGN (BIG PICTURE)
Login System
   ↓
Role-Based Dashboard
   ↓
(Teacher / Student / Admin)
   ↓
Analytics + AI Prediction + Data


🎨 2. UI DESIGN (LIKE YOUR IMAGE)
🔥 Layout Structure
📌 LEFT SIDEBAR (Main Navigation)
Dashboard
Classes
Subjects
Students
Attendance
Marks
Predictions (🔥 AI Feature)
Reports

📌 TOP NAVBAR
☰ Menu button (collapse sidebar)
User profile (right side)
Logout


📌 MAIN CONTENT AREA
Cards (stats)
Tables (data)
Graphs (later)


🧱 3. YOUR DASHBOARD STRUCTURE
👨‍🏫 TEACHER DASHBOARD
🔹 Cards
Total Students
Total Classes
At-Risk Students 🚨
Average Performance


🔹 Sections
📚 Classes
Create class
View class list
Show class code
📖 Subjects
Add subject
View subjects
👨‍🎓 Students
List students
Filter by class


📊 Marks
Enter marks
View marks
🤖 Predictions (MAIN FEATURE)
Show:
Risk Level (Low / Medium / High)
Reason (Low attendance etc

👨‍🎓 STUDENT DASHBOARD
🔹 Cards
Attendance %
Avg Marks
Risk Level 🚨
🔹 Sections
Join Class
View Subjects
View Marks
View Prediction
Study Suggestions (later)
🎯 4. UI FEATURES YOU MUST ADD
✅ Sidebar toggle (☰ like image)
✅ Back button everywhere
✅ Cards UI
✅ Tables (not plain text)

✅ Colors:
Green → Safe
Yellow → Medium
Red → Risk



🧱 FINAL STRUCTURE (CLEAN)
project/
│
├── app.py
├── templates/
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── base.html
│   ├── teacher_dashboard.html
│   ├── student_dashboard.html
│
├── static/
│   ├── style.css        ← for auth pages
│   ├── dashboard.css    ← for dashboard
│   ├── script.js



























