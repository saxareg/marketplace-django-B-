# 🛠️ Seller API Documentation

This API allows **authenticated sellers** to manage their own shops and products.

All endpoints are under `/api/seller/` and require JWT authentication.

---

## 🔐 Authentication

Get a JWT token:

```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -d "username=seller1" \
  -d "password=12345"
```

Use the access token in subsequent requests:

```bash
-H "Authorization: Bearer <ACCESS_TOKEN>"
```

---

## 🏪 Manage Shops

### 1. Get your shops

```bash
curl -X GET http://127.0.0.1:8000/api/seller/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

### 2. Update a shop by slug

```bash
curl -X PATCH http://127.0.0.1:8000/api/seller/minsk-market/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"name": "Магазин Обновлён"}'
```

---

## 📦 Manage Products (per shop)

All product actions are scoped under the seller's shop:

### 1. List products

```bash
curl -X GET http://127.0.0.1:8000/api/seller/minsk-market/products/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

### 2. Create a product

```bash
curl -X POST http://127.0.0.1:8000/api/seller/minsk-market/products/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Новый товар от продавца",
    "slug": "new-seller-product",
    "description": "Тестовое описание",
    "price": "999.99",
    "category": 49
  }'
```

### 3. Retrieve a specific product

```bash
curl -X GET http://127.0.0.1:8000/api/seller/minsk-market/products/<product_slug>/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

### 4. Update a product (partial)

```bash
curl -X PATCH http://127.0.0.1:8000/api/seller/minsk-market/products/<product_slug>/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"price": "888.88"}'
```

### 5. Delete a product

```bash
curl -X DELETE http://127.0.0.1:8000/api/seller/minsk-market/products/<product_slug>/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

---

## 🧾 Notes

- You can only access and modify **your own shops** and their products.
- If you try to access or mutate other seller’s resources, you’ll get `403 Forbidden`.

---

## 🛡️ Permissions

All endpoints require:

- JWT token (`Authorization: Bearer ...`)
- Authenticated user must own the shop they work with.
