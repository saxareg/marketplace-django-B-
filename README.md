# marketplace-django
website-marketplace for team diplom project

## Setup
-  go to a folder to place the marketplace project
```bash
git clone https://github.com/BogdanMalashuk/marketplace-django.git
cd marketplace-django

git switch develop

python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
source source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

touch .env
```
- put following in the .env file

```bash
# Django settings
SECRET_KEY='{your_django_key_here}'
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Celery settings
CELERY_BROKER_URL='redis://localhost:6379/0'  # 'localhost' -> 'redis' for docker usage 
CELERY_RESULT_BACKEND='redis://localhost:6379/0'  # 'localhost' -> 'redis' for docker usage

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

# Database settings for sqlite3
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# Database settings for Postgres
# DB_ENGINE=django.db.backends.postgresql
# DB_NAME=your_db_name
# DB_USER=your_db_user
# DB_PASSWORD=your_db_password
# DB_HOST=localhost
# DB_PORT=5432
```

- check docker
```
docker --version
```
> Docker version 28.1.1, build 4eba377```

- build images
```bash
docker-compose build
```

- run containers
```
docker-compose up -d
```

- prefill database with demo items 
```
docker-compose exec web python project/manage.py seed_data
```

- for non docker usage:
```
cd project
```

- prefill database with demo items 
```
manage.py seed_data
```

- create superuser
```
python manage.py create_admin
```
> Superuser "admin" has been created.
> User profile for superuser "admin" has been created.

- register periodic task(s)
```
python manage.py register_periodic_tasks
```
> Periodic task "mark_unclaimed_orders_every_day" registered successfully.


## Database Seeding Script
The `seed_database` Django command fills a marketplace database with test data to enable testing, development, and feature demonstration.

### Usage

The script is included in the project. To run it, ensure your Django project is set up with migrations applied, then execute:
```bash
python manage.py seed_database
```

### Seeding Steps

The script performs the following steps, logged as they complete:
- **1/9: Clearing Existing Data** — Deletes all non-superuser data from models (`User`, `UserProfile`, `PickupPoints`, `Category`, `Shop`, `Product`, `Cart`, `Order`, `Review`) to ensure a clean database.
- **2/9: Creating Pickup Points** — Adds 10 pickup points in various cities, each with a unique address, description, operating hours, and an associated staff user with a `UserProfile` set to `pp_staff` role.
- **3/9: Creating Categories** — Sets up 8 product categories (e.g., Electronics, Clothing, Books, Appliances) with names, slugs, and descriptive text for filtering products.
- **4/9: Creating Users and Profiles** — Creates 10 buyer users and 5 seller users, each with a `UserProfile` specifying their role (`buyer` or `seller`) and linked to a unique email and username.
- **5/9: Creating Shops** — Adds 5 shops (2 general-purpose, 3 specialized) with names, slugs, descriptions, active status, and assigned seller owners.
- **6/9: Creating Products** — Generates 40 products across shops and categories, including items like smartphones, clothing, books, and sports equipment, with prices, stock quantities, and active status.
- **7/9: Creating Carts and CartItems** — Sets up shopping carts for 5 buyers, each containing multiple products with specified quantities, linked to their respective user accounts.
- **8/9: Creating Orders and OrderItems** — Creates 15 orders for 6 buyers, linked to specific shops and pickup points, with varied statuses (e.g., pending, delivered, returned) and order items detailing products, quantities, and prices.
- **9/9: Creating Reviews** — Adds 10 product reviews from buyers, including ratings (2–5) and comments, tied to products from completed orders, with timestamps for realism.
