# 📘 Marketplace Public API Documentation (Read-Only)

This document describes the **Marketplace Public API** — a public, read-only REST API that allows users to access information about categories, shops, and products. The API supports filtering, searching, sorting, and pagination.

All endpoints are accessible under the `/api/public/` prefix.

---

## 🏢 Base URL

```
http://<your-domain>/api/public/
```

Example for local development:

```
http://127.0.0.1:8000/api/public/
```

---

## 🔢 Endpoints

| Endpoint               | Method | Description                      |
|------------------------|--------|----------------------------------|
| `/public/categories/` | GET    | List all categories              |
| `/public/shops/`      | GET    | List all shops                   |
| `/public/products/`   | GET    | List all products (with filters) |

---

## 📚 List All Categories

```bash
curl http://127.0.0.1:8000/api/public/categories/
```

---

## 🏬 List All Shops

```bash
curl http://127.0.0.1:8000/api/public/shops/
```

---

## 📦 List Products (with Filters)

```bash
curl -G http://127.0.0.1:8000/api/public/products/   --data-urlencode "category__slug=electronics"
```

### 🔍 Filtering Options

| Parameter            | Type    | Description                                     |
|----------------------|---------|-------------------------------------------------|
| `category__slug`     | string  | Filter by category slug (exact)                 |
| `category__slug__in` | list    | Filter by multiple categories (comma-separated) |
| `shop__slug`         | string  | Filter by shop slug                             |
| `shop__slug__in`     | list    | Filter by multiple shops                        |
| `search`             | string  | Search by product name (partial match)          |
| `ordering`           | string  | Sort by field (e.g. `price`, `-name`)           |
| `page`               | integer | Page number for pagination                      |

> ⚠️ Note: at least one category filter (`category__slug` or `category__slug__in`) is **required**.

### 🔄 Example Requests

**Search by product name**

```bash
curl -G http://127.0.0.1:8000/api/public/products/   --data-urlencode "category__slug=electronics"   --data-urlencode "search=Samsung"
```

**Sort by price descending**

```bash
curl -G http://127.0.0.1:8000/api/public/products/   --data-urlencode "category__slug=electronics"   --data-urlencode "ordering=-price"
```

**Pagination (page 2)**

```bash
curl -G http://127.0.0.1:8000/api/public/products/   --data-urlencode "category__slug=electronics"   --data-urlencode "page=2"
```

**Multiple categories via `category__slug__in`**

```bash
curl -G http://127.0.0.1:8000/api/public/products/   --data-urlencode "category__slug__in=electronics,books"
```

**Multiple shops via `shop__slug__in`**

```bash
curl -G http://127.0.0.1:8000/api/public/products/   --data-urlencode "category__slug=electronics"   --data-urlencode "shop__slug__in=techtrend,minsk-market"
```

**Error for unknown category**

```bash
curl -G http://127.0.0.1:8000/api/public/products/   --data-urlencode "category__slug=notexist"
```

Expected response:

```json
{
  "detail": "Category with slug 'notexist' does not exist."
}
```

---

## 📊 Response Format

Example (paginated):

```json
{
  "count": 28,
  "next": "http://.../products/?page=2",
  "previous": null,
  "results": [
    {
      "id": 123,
      "name": "Smartphone Samsung A54",
      "slug": "samsung-a54",
      "description": "...",
      "price": "1200.00",
      "category": {"id": 1, "name": "Electronics", "slug": "electronics"},
      "shop": {"id": 2, "name": "TechTrend", "slug": "techtrend"}
    }
  ]
}
```

---

## 🚀 Pagination

Enabled by default:

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
```

Use `?page=N` to paginate.

---

## 🛡 License & Auth

This API is **public and read-only**. No authentication required.
