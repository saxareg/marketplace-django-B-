# 🛍️ Marketplace Seller API Documentation

This document describes the **Marketplace Seller API** — a protected, write-enabled API that allows sellers to manage their own shops and products.

All endpoints are accessible under the `/api/seller/` prefix.

---

## 🔐 Authentication

All requests to Seller API **require JWT authentication**.

Obtain token via:
```bash
POST /api/token/
```

Use the `access` token in headers:
```
Authorization: Bearer <your-token>
```

---

## 🧭 Endpoints Overview

| Endpoint                            | Method | Description                          |
|-------------------------------------|--------|--------------------------------------|
| `/api/seller/`                      | GET    | Get list of seller's own shops       |
| `/api/seller/<shop_slug>/`         | PATCH  | Update shop info                     |
| `/api/seller/<shop_slug>/products/`| GET    | List products in the shop            |
| `/api/seller/<shop_slug>/products/`| POST   | Create a new product in the shop     |

---

## 🛒 Shop Management

### 🔹 Get list of own shops
```bash
curl -X GET http://127.0.0.1:8000/api/seller/   -H "Authorization: Bearer <token>"
```

### 🔹 Update a shop
```bash
curl -X PATCH http://127.0.0.1:8000/api/seller/minsk-market/   -H "Authorization: Bearer <token>"   -H "Content-Type: application/json"   -d '{"name": "Минск Маркет Обновлённый"}'
```

---

## 📦 Product Management

### 🔹 Get products in your shop
```bash
curl -X GET http://127.0.0.1:8000/api/seller/minsk-market/products/   -H "Authorization: Bearer <token>"
```

### 🔹 Create a product in your shop
```bash
curl -X POST http://127.0.0.1:8000/api/seller/minsk-market/products/   -H "Authorization: Bearer <token>"   -H "Content-Type: application/json"   -d '{
    "name": "Новый товар от продавца",
    "slug": "new-seller-product",
    "description": "Тестовое описание",
    "price": "999.99",
    "category": 49
  }'
```

> Note: You don’t need to provide `shop` explicitly — it is auto-attached from URL path and authenticated user.

---

## 🛡️ Permissions & Validation

- All endpoints require **valid JWT token**.
- Sellers can access and modify **only their own shops and products**.
- Attempts to access or modify others' data will return `403 Forbidden`.
