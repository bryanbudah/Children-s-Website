# 🌟 Children's Home Website

A Django-based web application designed to provide educational and engaging content for children. This project focuses on a clean, user-friendly interface with secure backend functionality.

---

## 🚀 Features

- User authentication (login & registration)
- Admin-managed content (articles, courses, events)
- Responsive design for mobile and desktop
- Commenting and interaction system
- Secure backend using Django

---

## 🛠️ Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite (default, can be upgraded)
- **Styling:** Tailwind CSS (optional)

---

## 📦 Installation

### 1. Clone the repository
```bash
git clone <your-repo-link>
cd children's home
childrens_home/
│
├── childrens_home/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── core/                # homepage and general pages
│   ├── views.py
│   ├── urls.py
│   └── templates/
│
├── children/            # children profiles
│   ├── models.py
│   ├── views.py
│   └── admin.py
│
├── donations/           # donations + mpesa
│   ├── models.py
│   ├── views.py
│   └── services.py
│
├── events/              # charity events
│   ├── models.py
│   └── admin.py
│
├── accounts/            # donor accounts
│   ├── models.py
│   └── views.py
│
├── templates/
│   ├── base.html
│   └── home.html
│
├── static/
│
├── media/
│
└── manage.py