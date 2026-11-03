# 🩸 BloodConnect – Blood Donor Management System

**BloodConnect** is a web-based blood donor management system developed using Django. It aims to connect people who need blood with registered donors based on blood group and location.

The system provides donor registration, blood group search, blood request management, and staff administration through a simple and user-friendly interface.

## 🌟 Features

- **User Registration and Login:** Users can create accounts and securely log in.
- **Donor Registration:** Donors can provide their details, including blood group, age, gender, location, and availability.
- **Blood Group Search:** Search for donors based on blood group and location.
- **Blood Request Management:** Users can send blood requests to registered donors.
- **Request Status Tracking:** Donors can manage incoming requests and update their status.
- **Staff Administration:** Staff can manage donor records through the Django admin panel.
- **Responsive Interface:** Simple interface designed for easy navigation.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Django | Web framework |
| HTML | Page structure |
| CSS | Styling |
| Bootstrap | Responsive design |
| PostgreSQL | Production database |
| SQLite | Local development database |
| Git & GitHub | Version control |
| Render | Deployment |
| Supabase | Hosted PostgreSQL database |

## 📂 Project Structure

```text
BloodConnect/
│
├── bloodconnect/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── donors/
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── templates/
├── static/
│   └── css/
│
├── .env.example
├── .gitignore
├── build.sh
├── render.yaml
├── manage.py
├── requirements.txt
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/jesmi29/BloodConnect.git
```

### 2. Navigate to the project folder

```bash
cd BloodConnect
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment (Windows)

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure environment variables

Create a `.env` file using `.env.example` as a reference. Configure your local development settings and database credentials securely. Never upload `.env` or passwords to GitHub.

### 7. Apply database migrations

```bash
python manage.py migrate
```

### 8. Create an admin account (optional)

```bash
python manage.py createsuperuser
```

### 9. Run the development server

```bash
python manage.py runserver
```

Open the application in your browser:

```text
http://127.0.0.1:8000/
```

## 🌐 Live Deployment

**Live Website:** https://bloodconnect-abei.onrender.com

**GitHub Repository:** https://github.com/jesmi29/BloodConnect

The application is deployed using Render with a PostgreSQL database hosted on Supabase.

## 🔐 Security and Privacy

- Environment variables are used to store sensitive configuration.
- Database credentials and secret keys should never be committed to GitHub.
- Donor contact information should be protected.
- This project is an academic demonstration and is not a verified medical or emergency service.

## 🎯 Project Objective

The main objective of BloodConnect is to simplify the process of finding blood donors by providing a centralized platform where users can search for donors and manage blood requests efficiently.

## 👩‍💻 Developer

**Jesmi S**  
B.Sc. Information Technology  
Sri Ramakrishna College of Arts And Science For Womens
