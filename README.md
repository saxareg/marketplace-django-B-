# 🛒 Marketplace Django

A full-featured web marketplace platform built with Django for a university diploma team project. It includes product listings, user roles (buyers, sellers, pickup staff), shopping carts, orders, reviews, and periodic tasks.

---

## 📌 Project Features

- 🔐 Role-based user system (Admin, Buyer, Seller, Pickup Staff)
- 🛍️ Shop creation and product management
- 🛒 Shopping cart and checkout system
- 📦 Order tracking with pickup/delivery
- 💬 Product reviews
- ⏱️ Scheduled tasks using Celery + Redis
- 🖼️ Media upload support (images for shops/products)
- 📊 Admin panel at `/custom_admin/`
- 🗄️ SQLite/PostgreSQL support (via `.env`)

---

## 🚧 Known Limitations

See [`project/docs/known_limitations.md`](project/docs/known_limitations.md) for a list of current limitations and open points during MVP development.

---

## 🧭 Project Structure

```
marketplace-django/
├── app_users/           # User profiles, roles, and authentication
├── app_shops/           # Shops and shop creation requests
├── app_products/        # Product categories, products, reviews
├── app_orders/          # Carts, orders, order items
├── project/             # Main Django project config
├── media/               # Uploaded media files
└── project/docs/        # Documentation and data model
```

---

## 🖼️ Data Model Overview

![Marketplace Data Model](project/docs/models.png)

The project follows a modular domain-driven architecture, with foreign key relationships connecting shops, users, products, and orders.

---

## 🛠️ Installation

Setup instructions (virtual environment, `.env`, dependencies, Docker, etc.):  
📄 [`project/docs/installation_manual.md`](project/docs/installation_manual.md)

---

## 🐳 Docker Support

The project includes a full Docker-based setup for local development and testing.

### Services:

| Service        | Description                                 |
|----------------|---------------------------------------------|
| `web`          | Django application running on port `8000`   |
| `celery`       | Celery worker processing background jobs    |
| `celery-beat`  | Celery Beat scheduler for periodic tasks    |
| `redis`        | Redis as Celery broker and result backend   |

### Common Commands:

```bash
# Build and start all services
docker-compose up -d --build

# Stop all containers
docker-compose down

# View logs
docker-compose logs -f

# Seed database with data 
docker-compose exec web python manage.py seed_data

```
> ⚠️ Make sure `.env` is properly configured before running Docker services.


---

## 🌱 Database Seeding

Command to populate the database with test data (users, products, shops, orders):  
📄 [`project/docs/seed_data.md`](project/docs/seed_data.md)

Usage example:

```bash
python manage.py seed_data
```

---

## ⚙️ Celery & Periodic Tasks

This project uses **Celery** with **Redis** for background task processing, and **Celery Beat** for scheduling periodic jobs.

📄 See all tasks in [`project/docs/celery_tasks.md`](project/docs/celery_tasks.md)

### Active Scheduled Task:

| Task Name                             | Description                                        |
|--------------------------------------|----------------------------------------------------|
| `app_orders.tasks.mark_unclaimed_orders` | Marks unpaid orders as "unclaimed" after 7 days |

To register the periodic task:

```bash
python manage.py register_periodic_tasks
```

> ✅ Periodic task `mark_unclaimed_orders_every_day` will be registered successfully.

---

## 📮 Admin Access

The admin interface is available at:  
🔗 [`https://<your-domain>/custom_admin/`](https://<your-domain>/custom_admin/)

Default superuser credentials:

| Username | Password |
|----------|----------|
| `admin`  | `admin`  |

---

## 📚 Additional Docs

| Topic                    | File                                        |
|--------------------------|---------------------------------------------|
| Installation Guide       | [`installation_manual.md`](project/docs/installation_manual.md) |
| Seed Data (Users, Orders)| [`seed_data.md`](project/docs/seed_data.md)     |
| Data Model Diagram       | [`models.png`](project/docs/models.png)         |
| Known Limitations        | [`known_limitations.md`](project/docs/known_limitations.md)     |
| Celery Tasks             | [`celery_tasks.md`](project/docs/celery_tasks.md) |

---

## 👥 Authors

This project is developed by the [Diploma Team].  
You are welcome to contribute, test, or reuse the code for educational purposes.
