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




🗓️ DAY 1 (8 HOURS) — 🧱 FOUNDATION + UI
🎯 Goal: Clean system + visible data
Fix dashboard UI (sidebar, cards, sections)
Show:
Classes list
Students list
Ensure:
Create class ✅
Join class ✅
Add subject ✅

👉 Output: Working clean UI + basic system


🗓️ DAY 2 (8 HOURS) — 💪 CORE FEATURES
🎯 Goal: Data system complete
Create marks table
Teacher enters marks manually
Student views marks
Add attendance field

👉 Output:

Marks working ✅
Attendance working ✅


🗓️ DAY 3 (6 HOURS) — 🤖 AI SYSTEM
🎯 Goal: Prediction system
Build simple ML model:
Input: marks + attendance
Output: risk (0/1)
Show in dashboard:
Green → Safe
Red → At Risk

👉 Output:

AI working ✅
Dashboard showing prediction ✅

🗓️ DAY 4 (4 HOURS) — 🔥 ADVANCED FEATURES
🎯 Goal: Make project stand out
👨‍🏫 Feature 1: CSV / Excel Upload
Upload file
Parse using pandas
Insert into DB

👉 Bulk data entry (VERY IMPRESSIVE)

👨‍🎓 Feature 2: Performance Graph
Use Chart.js
Show marks visually

👉 Makes UI look modern + smart

🗓️ DAY 5 — 🎯 FINALIZATION + SUBMISSION
🎯 Goal: Clean & presentable project
Fix bugs
Improve UI spacing
Add:
success messages
proper navigation
Push final code to GitHub
Add README


🧠 FINAL PROJECT FEATURES (AFTER 5 DAYS)

Your project will have:

✅ Login system
✅ Teacher dashboard
✅ Student dashboard
✅ Class & subject system
✅ Marks + attendance
✅ 🤖 AI prediction
✅ 📂 CSV/Excel upload
✅ 📊 Performance graph
✅ Clean UI
✅ GitHub repo


### on 10/04/26
🎯 WHAT YOU WANT TO BUILD
👨‍🏫 Teacher:
Add marks for students
Assign marks per subject
👨‍🎓 Student:
Automatically get subjects
View their marks
🧠 IMPORTANT DESIGN (VERY CLEAN APPROACH)

We’ll follow real-world logic:

✅ FLOW
1. Teacher creates:
Class ✅
Subjects ✅
2. Student joins class:

➡️ Automatically gets all subjects of that class

3. Teacher enters marks:

➡️ Select:

Student
Subject
Enter marks

4. Student dashboard:

➡️ See:

Subject-wise marks
(Later → graphs 📊)
