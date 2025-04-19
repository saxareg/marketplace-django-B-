from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app_users.models import UserProfile, PickupPoints
from app_shops.models import Shop
from app_products.models import Category, Product, Review
from app_orders.models import Cart, CartItem, Order, OrderItem

class Command(BaseCommand):
    help = 'Seeds the database with test data for Belarus marketplace'

    def handle(self, *args, **kwargs):
        # Очистка данных (кроме суперпользователей)
        User.objects.exclude(is_superuser=True).delete()
        PickupPoints.objects.all().delete()
        Category.objects.all().delete()
        Shop.objects.all().delete()
        Product.objects.all().delete()
        Cart.objects.all().delete()
        Order.objects.all().delete()
        Review.objects.all().delete()

        # 1. PickupPoints (10 штук, в ТЦ Беларуси)
        pickup_points = [
            {"city": "Минск", "street": "пр-т Победителей, 9", "postal_code": "220004", "description": "ТЦ Galleria Minsk, 10:00-22:00", "is_active": True, "name": "Минск - ПВЗ #1"},
            {"city": "Минск", "street": "пр-т Дзержинского, 106", "postal_code": "220116", "description": "ТЦ Magnit, 10:00-21:00", "is_active": True, "name": "Минск - ПВЗ #2"},
            {"city": "Минск", "street": "ул. Притыцкого, 156", "postal_code": "220017", "description": "ТЦ Green City, 10:00-22:00", "is_active": True, "name": "Минск - ПВЗ #3"},
            {"city": "Минск", "street": "ул. Немига, 5", "postal_code": "220030", "description": "ТЦ Метрополь, 10:00-21:00", "is_active": True, "name": "Минск - ПВЗ #4"},
            {"city": "Гродно", "street": "ул. Советская, 29", "postal_code": "230023", "description": "ТЦ Неман, 10:00-20:00", "is_active": True, "name": "Гродно - ПВЗ #5"},
            {"city": "Брест", "street": "ул. Московская, 210", "postal_code": "224030", "description": "ТЦ Корона, 09:00-21:00", "is_active": True, "name": "Брест - ПВЗ #6"},
            {"city": "Витебск", "street": "пр-т Строителей, 15", "postal_code": "210027", "description": "ТЦ Марко-Сити, 10:00-20:00", "is_active": True, "name": "Витебск - ПВЗ #7"},
            {"city": "Гомель", "street": "ул. Советская, 97", "postal_code": "246050", "description": "ТЦ Секрет, 10:00-21:00", "is_active": True, "name": "Гомель - ПВЗ #8"},
            {"city": "Могилёв", "street": "ул. Ленинская, 83", "postal_code": "212030", "description": "ТЦ Панорама, 10:00-20:00", "is_active": True, "name": "Могилёв - ПВЗ #9"},
            {"city": "Бобруйск", "street": "ул. Минская, 133", "postal_code": "213809", "description": "ТЦ Корона, 09:00-21:00", "is_active": True, "name": "Бобруйск - ПВЗ #10"},
        ]
        pvz_objects = []
        # Создание пользователей для ПВЗ и привязка через UserProfile
        for i, point in enumerate(pickup_points, 1):
            # Создаём пользователя для ПВЗ
            pvz_username = f"pvz_worker_{point['name'].lower().replace(' ', '_').replace('#', '')}"
            pvz_user = User.objects.create_user(
                username=pvz_username,
                email=f"mktplc-pvz_{i}@mailinator.com",
                password="12345"
            )
            # Создаём ПВЗ
            point_obj = PickupPoints.objects.create(
                city=point["city"],
                street=point["street"],
                postal_code=point["postal_code"],
                description=point["description"],
                is_active=point["is_active"],
                name=point["name"]
            )
            # Привязываем пользователя к ПВЗ через UserProfile
            UserProfile.objects.create(
                user=pvz_user,
                role="pp_staff",
                pickup_point=point_obj
            )
            pvz_objects.append(point_obj)

        # 2. Categories (8 штук)
        categories = [
            {"name": "Электроника", "slug": "electronics", "description": "Смартфоны, ноутбуки, аксессуары"},
            {"name": "Одежда", "slug": "clothing", "description": "Мужская, женская и детская одежда"},
            {"name": "Книги", "slug": "books", "description": "Художественная и учебная литература"},
            {"name": "Бытовая техника", "slug": "appliances", "description": "Техника для дома и кухни"},
            {"name": "Спорт", "slug": "sports", "description": "Спортивные товары и аксессуары"},
            {"name": "Косметика", "slug": "cosmetics", "description": "Средства для ухода и макияжа"},
            {"name": "Игрушки", "slug": "toys", "description": "Игрушки для детей всех возрастов"},
            {"name": "Продукты питания", "slug": "food", "description": "Продукты и напитки"},
        ]
        for cat in categories:
            Category.objects.create(**cat)

        # 3. Users and Profiles (10 покупателей, 5 продавцов)
        # Покупатели
        buyers = []
        for i in range(1, 11):
            user = User.objects.create_user(
                username=f"buyer{i}",
                email=f"mktplc-user_{i}@mailinator.com",
                password="12345"
            )
            UserProfile.objects.create(user=user, role="buyer")
            buyers.append(user)

        # Продавцы
        sellers = []
        for i in range(1, 6):
            user = User.objects.create_user(
                username=f"seller{i}",
                email=f"mktplc-user_seller{i}@mailinator.com",
                password="12345"
            )
            UserProfile.objects.create(user=user, role="seller")
            sellers.append(user)

        # 4. Shops (5 штук: 2 общих, 3 узких)
        shops = [
            {
                "name": "Минск Маркет",
                "slug": "minsk-market",
                "owner": sellers[0],
                "description": "Гипермаркет товаров: электроника, одежда, продукты. Работает Пн-Вс 09:00-22:00. Доставка по Минску.",
                "is_active": True,
            },
            {
                "name": "Беларусь Универсал",
                "slug": "belarus-universal",
                "owner": sellers[1],
                "description": "Широкий ассортимент: техника, игрушки, косметика. Работает Пн-Сб 10:00-21:00. Самовывоз из ТЦ.",
                "is_active": True,
            },
            {
                "name": "TechTrend",
                "slug": "techtrend",
                "owner": sellers[2],
                "description": "Магазин электроники: смартфоны, ноутбуки, аксессуары. Работает Пн-Вс 10:00-20:00. Гарантия 1 год.",
                "is_active": True,
            },
            {
                "name": "BookHaven",
                "slug": "bookhaven",
                "owner": sellers[3],
                "description": "Книжный магазин: художественная, учебная литература. Работает Пн-Пт 09:00-19:00, Сб 10:00-16:00.",
                "is_active": True,
            },
            {
                "name": "SportZone",
                "slug": "sportzone",
                "owner": sellers[4],
                "description": "Спортивные товары: одежда, тренажёры, аксессуары. Работает Пн-Вс 10:00-21:00. Бесплатная консультация.",
                "is_active": True,
            },
        ]
        shop_objects = []
        for shop in shops:
            shop_obj = Shop.objects.create(**shop)
            shop_objects.append(shop_obj)

        # 5. Products (40 штук, распределены по магазинам и категориям)
        products = [
            # Минск Маркет (общий, 10 товаров)
            {"shop": shop_objects[0], "category": Category.objects.get(slug="electronics"), "name": "Смартфон Samsung", "slug": "samsung-phone", "description": "Samsung Galaxy A54, 128 ГБ", "price": 1200, "stock": 15, "is_active": True},
            {"shop": shop_objects[0], "category": Category.objects.get(slug="electronics"), "name": "Ноутбук Lenovo", "slug": "lenovo-laptop", "description": "Lenovo IdeaPad 3, 16 ГБ RAM", "price": 2500, "stock": 8, "is_active": True},
            {"shop": shop_objects[0], "category": Category.objects.get(slug="clothing"), "name": "Куртка мужская", "slug": "mens-jacket", "description": "Зимняя куртка, размер M", "price": 200, "stock": 20, "is_active": True},
            {"shop": shop_objects[0], "category": Category.objects.get(slug="clothing"), "name": "Джинсы женские", "slug": "womens-jeans", "description": "Джинсы slim, размер 28", "price": 150, "stock": 25, "is_active": True},
            {"shop": shop_objects[0], "category": Category.objects.get(slug="books"), "name": "Книга '1984'", "slug": "book-1984", "description": "Роман Дж. Оруэлла", "price": 30, "stock": 30, "is_active": True},
            {"shop": shop_objects[0], "category": Category.objects.get(slug="appliances"), "name": "Микроволновка", "slug": "microwave", "description": "Микроволновая печь 20 л", "price": 300, "stock": 10, "is_active": True},
            {"shop": shop_objects[0], "category": Category.objects.get(slug="cosmetics"), "name": "Крем для лица", "slug": "face-cream", "description": "Увлажняющий крем 50 мл", "price": 50, "stock": 40, "is_active": True},
            {"shop": shop_objects[0], "category": Category.objects.get(slug="toys"), "name": "Конструктор LEGO", "slug": "lego-set", "description": "LEGO Classic 500 деталей", "price": 100, "stock": 15, "is_active": True},
            {"shop": shop_objects[0], "category": Category.objects.get(slug="food"), "name": "Шоколад Milka", "slug": "milka-chocolate", "description": "Молочный шоколад 100 г", "price": 5, "stock": 100, "is_active": True},
            {"shop": shop_objects[0], "category": Category.objects.get(slug="sports"), "name": "Фитнес-браслет", "slug": "fitness-tracker", "description": "Считает шаги и пульс", "price": 80, "stock": 20, "is_active": True},
            # Беларусь Универсал (общий, 10 товаров)
            {"shop": shop_objects[1], "category": Category.objects.get(slug="electronics"), "name": "Планшет Huawei", "slug": "huawei-tablet", "description": "Huawei MatePad, 64 ГБ", "price": 800, "stock": 12, "is_active": True},
            {"shop": shop_objects[1], "category": Category.objects.get(slug="electronics"), "name": "Наушники Sony", "slug": "sony-headphones", "description": "Беспроводные наушники", "price": 200, "stock": 25, "is_active": True},
            {"shop": shop_objects[1], "category": Category.objects.get(slug="clothing"), "name": "Футболка унисекс", "slug": "unisex-tshirt", "description": "Хлопковая футболка, размер L", "price": 40, "stock": 50, "is_active": True},
            {"shop": shop_objects[1], "category": Category.objects.get(slug="clothing"), "name": "Свитер женский", "slug": "womens-sweater", "description": "Тёплый свитер, размер S", "price": 120, "stock": 15, "is_active": True},
            {"shop": shop_objects[1], "category": Category.objects.get(slug="books"), "name": "Книга 'Дюна'", "slug": "book-dune", "description": "Роман Фрэнка Герберта", "price": 35, "stock": 20, "is_active": True},
            {"shop": shop_objects[1], "category": Category.objects.get(slug="appliances"), "name": "Чайник электрический", "slug": "electric-kettle", "description": "Чайник 1.7 л", "price": 100, "stock": 18, "is_active": True},
            {"shop": shop_objects[1], "category": Category.objects.get(slug="cosmetics"), "name": "Шампунь", "slug": "shampoo", "description": "Шампунь для волос 250 мл", "price": 20, "stock": 60, "is_active": True},
            {"shop": shop_objects[1], "category": Category.objects.get(slug="toys"), "name": "Мягкая игрушка", "slug": "soft-toy", "description": "Плюшевый медведь 30 см", "price": 50, "stock": 30, "is_active": True},
            {"shop": shop_objects[1], "category": Category.objects.get(slug="food"), "name": "Кофе Nescafe", "slug": "nescafe-coffee", "description": "Растворимый кофе 100 г", "price": 15, "stock": 80, "is_active": True},
            {"shop": shop_objects[1], "category": Category.objects.get(slug="sports"), "name": "Коврик для йоги", "slug": "yoga-mat", "description": "Коврик 6 мм", "price": 60, "stock": 25, "is_active": True},
            # TechTrend (электроника, 8 товаров)
            {"shop": shop_objects[2], "category": Category.objects.get(slug="electronics"), "name": "Телевизор LG", "slug": "lg-tv", "description": "Smart TV 43 дюйма", "price": 1500, "stock": 10, "is_active": True},
            {"shop": shop_objects[2], "category": Category.objects.get(slug="electronics"), "name": "Игровая мышь", "slug": "gaming-mouse", "description": "Logitech G Pro", "price": 150, "stock": 30, "is_active": True},
            {"shop": shop_objects[2], "category": Category.objects.get(slug="electronics"), "name": "Клавиатура", "slug": "keyboard", "description": "Механическая клавиатура", "price": 200, "stock": 20, "is_active": True},
            {"shop": shop_objects[2], "category": Category.objects.get(slug="electronics"), "name": "SSD 1 ТБ", "slug": "ssd-1tb", "description": "Samsung SSD 1 ТБ", "price": 300, "stock": 15, "is_active": True},
            {"shop": shop_objects[2], "category": Category.objects.get(slug="electronics"), "name": "Power Bank", "slug": "power-bank", "description": "10000 мАч", "price": 80, "stock": 40, "is_active": True},
            {"shop": shop_objects[2], "category": Category.objects.get(slug="electronics"), "name": "Умные часы", "slug": "smart-watch", "description": "Xiaomi Mi Watch", "price": 250, "stock": 12, "is_active": True},
            {"shop": shop_objects[2], "category": Category.objects.get(slug="electronics"), "name": "Роутер Wi-Fi", "slug": "wifi-router", "description": "TP-Link Archer", "price": 120, "stock": 18, "is_active": True},
            {"shop": shop_objects[2], "category": Category.objects.get(slug="electronics"), "name": "Веб-камера", "slug": "webcam", "description": "Logitech C920", "price": 100, "stock": 25, "is_active": True},
            # BookHaven (книги, 6 товаров)
            {"shop": shop_objects[3], "category": Category.objects.get(slug="books"), "name": "Книга 'Война и мир'", "slug": "war-and-peace", "description": "Роман Л. Толстого", "price": 50, "stock": 15, "is_active": True},
            {"shop": shop_objects[3], "category": Category.objects.get(slug="books"), "name": "Книга 'Преступление и наказание'", "slug": "crime-and-punishment", "description": "Роман Ф. Достоевского", "price": 40, "stock": 20, "is_active": True},
            {"shop": shop_objects[3], "category": Category.objects.get(slug="books"), "name": "Книга 'Гарри Поттер'", "slug": "harry-potter", "description": "Дж. Роулинг, 1 часть", "price": 45, "stock": 25, "is_active": True},
            {"shop": shop_objects[3], "category": Category.objects.get(slug="books"), "name": "Учебник Python", "slug": "python-book", "description": "Программирование на Python", "price": 60, "stock": 10, "is_active": True},
            {"shop": shop_objects[3], "category": Category.objects.get(slug="books"), "name": "Книга 'Мастер и Маргарита'", "slug": "master-and-margarita", "description": "Роман М. Булгакова", "price": 35, "stock": 18, "is_active": True},
            {"shop": shop_objects[3], "category": Category.objects.get(slug="books"), "name": "Детская энциклопедия", "slug": "kids-encyclopedia", "description": "Энциклопедия для детей", "price": 30, "stock": 20, "is_active": True},
            # SportZone (спорт, 6 товаров)
            {"shop": shop_objects[4], "category": Category.objects.get(slug="sports"), "name": "Гантели 10 кг", "slug": "dumbbells-10kg", "description": "Пара гантелей 10 кг", "price": 100, "stock": 15, "is_active": True},
            {"shop": shop_objects[4], "category": Category.objects.get(slug="sports"), "name": "Велосипед горный", "slug": "mountain-bike", "description": "Велосипед 26 дюймов", "price": 800, "stock": 5, "is_active": True},
            {"shop": shop_objects[4], "category": Category.objects.get(slug="sports"), "name": "Спортивная форма", "slug": "sportswear", "description": "Комплект для бега, размер M", "price": 120, "stock": 20, "is_active": True},
            {"shop": shop_objects[4], "category": Category.objects.get(slug="sports"), "name": "Тренажёр эллиптический", "slug": "elliptical-trainer", "description": "Домашний тренажёр", "price": 1000, "stock": 3, "is_active": True},
            {"shop": shop_objects[4], "category": Category.objects.get(slug="sports"), "name": "Мяч футбольный", "slug": "football-ball", "description": "Мяч размер 5", "price": 50, "stock": 30, "is_active": True},
            {"shop": shop_objects[4], "category": Category.objects.get(slug="sports"), "name": "Рюкзак спортивный", "slug": "sports-backpack", "description": "Рюкзак 20 л", "price": 80, "stock": 25, "is_active": True},
        ]
        for prod in products:
            Product.objects.create(**prod)

        self.stdout.write(self.style.SUCCESS("Тестовые данные успешно добавлены!"))
