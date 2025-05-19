# 🛠️ Installation Manual

Follow this guide to set up the Belarus Marketplace project for local development or Docker-based deployment.

---

## 📥 Clone the Project

```bash
git clone https://github.com/BogdanMalashuk/marketplace-django.git
cd marketplace-django
git switch develop
```

---

## 🧪 Create and Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate       # Windows
# OR
source .venv/bin/activate     # Alt if .venv used
```

---

## 📦 Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## ⚙️ Environment Configuration

Create a `.env` file and add the following variables:

```ini
# Django settings
SECRET_KEY='{your_django_key_here}'
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Celery settings
CELERY_BROKER_URL='redis://localhost:6379/0'  # 'localhost' -> 'redis' for Docker usage
CELERY_RESULT_BACKEND='redis://localhost:6379/0'

# Email settings
EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER='marketplace.diplom@gmail.com'
EMAIL_HOST_PASSWORD='aatnutopvxyukzqr'
DEFAULT_FROM_EMAIL='marketplace.diplom@gmail.com'

# Superuser
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=marketplace.diplom@gmail.com
DJANGO_SUPERUSER_PASSWORD=admin

# Database settings (SQLite)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# Database settings (PostgreSQL)
# DB_ENGINE=django.db.backends.postgresql
# DB_NAME=your_db_name
# DB_USER=your_db_user
# DB_PASSWORD=your_db_password
# DB_HOST=localhost
# DB_PORT=5432
```

---

## 🐳 Docker Setup

### 🔍 Check Docker Installation

```bash
docker --version
```

> Example: Docker version 28.1.1, build 4eba377

### 🧱 Build Docker Images

```bash
docker-compose build
```

### ▶️ Run Containers

```bash
docker-compose up -d
```

---

## 🧪 Seed the Database

### 🐳 Using Docker:

```bash
docker-compose exec web python project/manage.py seed_data
```

### 💻 Without Docker:

```bash
cd project
python manage.py seed_data
```

---

## 👤 Create Superuser

```bash
python manage.py create_admin
```

> ✅ Superuser "admin" has been created.  
> ✅ User profile for superuser "admin" has been created.

---

## 🔁 Register Periodic Tasks

```bash
python manage.py register_periodic_tasks
```

> ✅ Periodic task "mark_unclaimed_orders_every_day" registered successfully.