# BloodConnect — Django Blood Donor Directory

College FSD project: blood-group search, donor registration, requests and status management.

## Run locally (Windows, VS Code)

1. Install Python 3.12+ and VS Code. Extract this ZIP, open its `bloodconnect_project` folder in VS Code.
2. Open **Terminal > New Terminal** and run:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py createsuperuser
$env:DEBUG="True"
.\.venv\Scripts\python.exe manage.py runserver
```

3. Visit http://127.0.0.1:8000/ and admin at http://127.0.0.1:8000/admin/.
4. Sign up as user A and create a donor profile. Sign out, sign up as user B, search and send a request. Log in as A to accept it.

## Deployment on Render (with PostgreSQL)

1. Push these extracted files to a GitHub repository. Do not commit `.env`, `db.sqlite3` or `.venv`.
2. Create a **persistent PostgreSQL database** on Render (or another supported provider). Copy its internal connection URL into the web service `DATABASE_URL` environment variable. Check current pricing/availability.
3. Create a Render Web Service from your GitHub repository. Set runtime to Python, build command `bash build.sh`, and start command `gunicorn bloodconnect.wsgi:application`. Alternatively use `render.yaml` as a blueprint and fill required variables.
4. Configure environment variables: `DJANGO_SECRET_KEY` (long random secret), `DEBUG=False`, `DATABASE_URL`, `ALLOWED_HOSTS=<your-service>.onrender.com`, and `CSRF_TRUSTED_ORIGINS=https://<your-service>.onrender.com`.
5. Deploy. The build command installs packages, collects static files and migrates the database.
6. For admin, run `python manage.py createsuperuser` using the provider's secure shell/one-off command facility if available. Do not put admin passwords in source code.
7. Test registration, donor search, requests and status updates on the public URL.

**Important:** SQLite on an ephemeral hosted filesystem loses data on redeployment. Use a persistent PostgreSQL database in production. This project is a college demo, not a verified medical or emergency service. Donor phone numbers are not exposed on public pages; further security, consent and moderation work is needed before collecting real users' data.

## Offline

Once dependencies are installed, the Django development server and pages work locally without internet. Other people cannot access the hosted website without internet. This is not an offline-sync PWA.
