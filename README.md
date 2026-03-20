# CareerAI — Django Full Stack (No React, No Node.js)

## Run with ONE terminal only

```
cd ai_career_django
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
copy .env.example .env         # then edit .env with your MySQL password
python manage.py makemigrations users resume jobs interview dashboard
python manage.py migrate
python manage.py seed_questions
python manage.py createsuperuser
python manage.py runserver
```

Open browser: http://127.0.0.1:8000/login/

## Pages
- /login/       — Login & Register
- /dashboard/   — Stats overview
- /resume/      — Upload PDF, analyze against JD
- /jobs/        — Track applications
- /interview/   — Mock interview Q&A
- /skills/      — Skill gap analysis
- /admin/       — Django admin panel
