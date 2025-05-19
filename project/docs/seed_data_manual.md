# 📦 `seed_data` Management Command — Usage Guide

This command initializes your local development database with realistic demo data for the Belarus Marketplace project. It’s ideal for testing, development, and internal presentations.

---

## 🚀 How to Run

```bash
# Docker
docker-compose exec web python manage.py seed_data

# Non-Docker (local venv)
python manage.py seed_data
```

---

## 🔐 Superuser Credentials

An admin account is automatically created:

| Username | Password | Role  | Email                           |
|----------|----------|-------|---------------------------------|
| `admin`  | `admin`  | Admin | marketplace.diplom@gmail.com    |

You can access the Django Admin at:  
➡️ `https://{domain}/custom_admin/`

---

## 🖼️ Adds Demo Images

Images are added for shops and products from the local `images/` folder.  
File matching is based on the slug of each object and uses the following filename format:

- Shops: `shop_<slug>.jpg`  
- Products: `product_<slug>.jpg`  

_Example_: `shop_minsk-market.jpg`, `product_samsung-galaxy-a54.jpg`

---

## 🏷️ Product Categories

The following 8 product categories are created:

- Electronics  
- Clothing  
- Books  
- Home Appliances  
- Sports  
- Cosmetics  
- Toys  
- Food & Beverages  

---

## 🏪 Pickup Points + Staff Accounts

| Pickup Point Name     | Location       | Username       | Password | Email                           |
|-----------------------|----------------|----------------|----------|----------------------------------|
| Минск - ПВЗ #1        | Galleria Minsk | `pp_worker_1`  | 12345    | mktplc-pp_1@mailinator.com       |
| Минск - ПВЗ #2        | TC Magnit      | `pp_worker_2`  | 12345    | mktplc-pp_2@mailinator.com       |
| Минск - ПВЗ #3        | Green City     | `pp_worker_3`  | 12345    | mktplc-pp_3@mailinator.com       |
| Минск - ПВЗ #4        | Metropol       | `pp_worker_4`  | 12345    | mktplc-pp_4@mailinator.com       |
| Гродно - ПВЗ #5       | TC Neman       | `pp_worker_5`  | 12345    | mktplc-pp_5@mailinator.com       |
| Брест - ПВЗ #6        | TC Korona      | `pp_worker_6`  | 12345    | mktplc-pp_6@mailinator.com       |
| Витебск - ПВЗ #7      | Marco City     | `pp_worker_7`  | 12345    | mktplc-pp_7@mailinator.com       |
| Гомель - ПВЗ #8       | TC Secret      | `pp_worker_8`  | 12345    | mktplc-pp_8@mailinator.com       |
| Могилёв - ПВЗ #9      | Panorama       | `pp_worker_9`  | 12345    | mktplc-pp_9@mailinator.com       |
| Бобруйск - ПВЗ #10    | TC Korona      | `pp_worker_10` | 12345    | mktplc-pp_10@mailinator.com      |

---

## 🛍️ Demo Shops + Sellers

| Shop Name         | Owner Username | Password | Email                                 | Slug              |
|-------------------|----------------|----------|----------------------------------------|-------------------|
| Minsk Market      | `seller1`      | 12345    | mktplc-user_seller1@mailinator.com     | `minsk-market`    |
| Belarus Universal | `seller2`      | 12345    | mktplc-user_seller2@mailinator.com     | `belarus-universal`|
| TechTrend         | `seller3`      | 12345    | mktplc-user_seller3@mailinator.com     | `techtrend`       |
| BookHaven         | `seller4`      | 12345    | mktplc-user_seller4@mailinator.com     | `bookhaven`       |
| SportZone         | `seller5`      | 12345    | mktplc-user_seller5@mailinator.com     | `sportzone`       |

---

## 👤 Buyers (Demo Customers)

| Username | Password | Email                             |
|----------|----------|------------------------------------|
| buyer1   | 12345    | mktplc-user_1@mailinator.com       |
| buyer2   | 12345    | mktplc-user_2@mailinator.com       |
| buyer3   | 12345    | mktplc-user_3@mailinator.com       |
| buyer4   | 12345    | mktplc-user_4@mailinator.com       |
| buyer5   | 12345    | mktplc-user_5@mailinator.com       |
| buyer6   | 12345    | mktplc-user_6@mailinator.com       |
| buyer7   | 12345    | mktplc-user_7@mailinator.com       |
| buyer8   | 12345    | mktplc-user_8@mailinator.com       |
| buyer9   | 12345    | mktplc-user_9@mailinator.com       |
| buyer10  | 12345    | mktplc-user_10@mailinator.com      |

---

## ✅ How to Include in README

In your main `README.md`, you can insert a link to this document like this:

```markdown
📚 [Click here for full seed data guide](docs/SEED_DATA.md)
```

Or embed part of it using:

```markdown
## Demo Data

See [`SEED_DATA.md`](docs/SEED_DATA.md) for full instructions on how to populate the development database with test users, shops, orders, etc.
```
