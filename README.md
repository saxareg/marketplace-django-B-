# marketplace-django
website-marketplace for team diplom project

## Setup
1. Create a virtual environment: `python3 -m venv .venv`
2. Activate it: `source .venv/bin/activate` (or `.\.venv\Scripts\activate` on Windows)
3. Install dependencies: `pip install -r requirements.txt`
4. Run the server: `python manage.py runserver`


## Database Seeding Script
The `seed_database.py` Django command fills a marketplace database with test data to enable testing, development, and feature demonstration.

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
