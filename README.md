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

## 🧭 Project Structure

```
marketplace-django/
├── app_users/           # User profiles, roles, and authentication
├── app_shops/           # Shops and shop creation requests
├── app_products/        # Product categories, products, reviews
├── app_orders/          # Carts, orders, order items
├── project/             # Main Django project config
├── media/               # Uploaded media files
└── docs/                # Documentation and data model
```

---

## 🖼️ Data Model Overview

![Marketplace Data Model](docs/models.png)

The project follows a modular domain-driven architecture, with foreign key relationships connecting shops, users, products, and orders.

---

## 🛠️ Installation

Setup instructions (virtual environment, `.env`, dependencies, Docker, etc.):  
📄 [`docs/installation_manual.md`](docs/installation_manual.md)

---

## 🌱 Database Seeding

Command to populate the database with test data (users, products, shops, orders):  
📄 [`docs/SEED_DATA.md`](docs/SEED_DATA.md)

Usage example:

```bash
python manage.py seed_data
```

---

## ⚙️ Periodic Tasks

Background jobs (e.g., marking unclaimed orders) are scheduled using Celery Beat.  
To register them:

```bash
python manage.py register_periodic_tasks
```

> ✅ Periodic task "mark_unclaimed_orders_every_day" registered successfully.

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

| Topic                    | File                                    |
|--------------------------|-----------------------------------------|
| Installation Guide       | [`installation_manual.md`](docs/installation_manual.md) |
| Seed Data (Users, Orders)| [`SEED_DATA.md`](docs/SEED_DATA.md)     |
| Data Model Diagram       | [`models.png`](docs/models.png)         |
| Known Limitations        | [`known_limitations.md`](docs/known_limitations.md)     |

---

## 🚧 Known Limitations

See [`docs/known_limitations.md`](docs/known_limitations.md) for a list of current limitations and open points during MVP development.

---

## 👥 Authors

This project is developed by the [Diploma Team].  
You are welcome to contribute, test, or reuse the code for educational purposes.
