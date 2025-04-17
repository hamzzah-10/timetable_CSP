# 🗓️ CSP-Based Timetable Generator (Django)

A Django project that uses Constraint Satisfaction Problem (CSP) techniques to automatically generate optimized school timetables based on user-defined inputs such as teachers, subjects, rooms, and time slots.

---

## 🚀 Features

- 🎯 Constraint-based timetable generation using Google OR-Tools
- 🏫 Handles classrooms, teachers, subjects, rooms, and time slots
- 📌 Avoids conflicts (teacher clashes, room clashes, etc.)
- 🧪 Supports lab-classroom distinction
- 📊 Stores generated timetable in the database with admin access

---

## 🛠️ Tech Stack

- Python 3.x
- Django (Backend & Admin Panel)
- OR-Tools (Constraint Solver)
- SQLite/PostgreSQL (customizable)
- HTML (for optional front-end template rendering)

---

## ⚙️ Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/csp-timetable-generator.git
   cd csp-timetable-generator
Create Virtual Environment

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
Install Dependencies

pip install -r requirements.txt
Apply Migrations

python manage.py makemigrations
python manage.py migrate
Create Superuser (for admin panel)

python manage.py createsuperuser
Run the Development Server


python manage.py runserver
Access Admin Panel Go to http://localhost:8000/admin and log in with your superuser credentials.


🧠 How It Works
Admin adds:

Classrooms

Teachers (linked with subjects)

Subjects

Rooms (lab/classroom)

Time slots

Run the generate_timetable() function

The solver:

Ensures no conflicts

Assigns valid (subject, teacher, room, time) to each class

Results are stored in the TimetableEntry model and can be viewed or exported.

📌 Sample Constraints Enforced
One subject per class per slot

Teacher can’t be in two places at once

Room capacity and availability

Labs should be held in lab rooms

Max sessions per class-subject

📂 Folder Structure
Copy
Edit
├── timetable/
│   ├── models.py
│   ├── views.py
│   ├── admin.py
│   └── ...
├── manage.py
├── requirements.txt
└── README.md
🧪 Future Improvements
Front-end UI for timetable preview

Drag-and-drop manual adjustments

Export to Excel/PDF

Multi-school support

AI-enhanced constraint handling




