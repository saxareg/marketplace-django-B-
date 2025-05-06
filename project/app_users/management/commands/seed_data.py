from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from app_users.models import UserProfile, PickupPoints
from app_shops.models import Shop
from app_products.models import Category, Product, Review
from app_orders.models import Cart, CartItem, Order, OrderItem

class Command(BaseCommand):
    help = 'Seeds the database with test data for Belarus marketplace'

    def handle(self, *args, **kwargs):
        # Очистка данных (кроме суперпользователей)
        self.stdout.write('Step 0/8: Clearing existing data')
        User.objects.exclude(is_superuser=True).delete()
        UserProfile.objects.all().delete()
        PickupPoints.objects.all().delete()
        Category.objects.all().delete()
        Shop.objects.all().delete()
        Product.objects.all().delete()
        Cart.objects.all().delete()
        Order.objects.all().delete()
        Review.objects.all().delete()

        # 1. PickupPoints (10 штук, в ТЦ Беларуси)
        self.stdout.write('Step 1/8: Creating Pickup Points')
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
        
        pp_objects = []
        for i, point in enumerate(pickup_points, 1):
            # Извлекаем номер PP из названия (ищем число после #)
            pp_number = ''.join(filter(str.isdigit, point['name'].split('#')[-1]))
            pp_username = f"pp_worker_{pp_number}"
            pp_user = User.objects.create_user(
                username=pp_username,
                email=f"mktplc-pp_{pp_number}@mailinator.com",
                password="12345"
            )
            point_obj = PickupPoints.objects.create(
                city=point["city"],
                street=point["street"],
                postal_code=point["postal_code"],
                description=point["description"],
                is_active=point["is_active"],
                name=point["name"]
            )
            UserProfile.objects.create(
                user=pp_user,
                role="pp_staff",
                pickup_point=point_obj
            )
            pp_objects.append(point_obj)

        # 2. Categories (8 штук)
        self.stdout.write('Step 2/8: Creating Categories')
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
        category_objects = []
        for cat in categories:
            category_obj = Category.objects.create(**cat)
            category_objects.append(category_obj)

        # 3. Users and Profiles (10 покупателей, 5 продавцов)
        self.stdout.write('Step 3/8: Creating Users and Profiles')
        buyers = []
        for i in range(1, 11):
            user = User.objects.create_user(
                username=f"buyer{i}",
                email=f"mktplc-user_{i}@mailinator.com",
                password="12345"
            )
            UserProfile.objects.create(user=user, role="buyer")
            buyers.append(user)

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
        self.stdout.write('Step 4/8: Creating Shops')
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
        self.stdout.write('Step 5/8: Creating Products')
        products = [
            {"shop": shop_objects[0], "category": category_objects[0], "name": "Смартфон Samsung - Galaxy A54", "slug": "samsung-galaxy-a54", "description": "Samsung Galaxy A54, 128 ГБ, 5G", "price": 1200, "stock": 15, "is_active": True},
            {"shop": shop_objects[0], "category": category_objects[0], "name": "Ноутбук Lenovo - IdeaPad 3", "slug": "lenovo-ideapad-3", "description": "Lenovo IdeaPad 3, 16 ГБ RAM, SSD 512 ГБ", "price": 2500, "stock": 8, "is_active": True},
            {"shop": shop_objects[0], "category": category_objects[1], "name": "Куртка Columbia - FrostPeak", "slug": "columbia-frostpeak", "description": "Зимняя куртка, размер M, водоотталкивающая", "price": 200, "stock": 20, "is_active": True},
            {"shop": shop_objects[0], "category": category_objects[1], "name": "Джинсы Levi's - 501 Slim", "slug": "levis-501-slim", "description": "Джинсы slim, размер 28, хлопок", "price": 150, "stock": 25, "is_active": True},
            {"shop": shop_objects[0], "category": category_objects[2], "name": "Книга Penguin - 1984", "slug": "penguin-1984", "description": "Роман Дж. Оруэлла, мягкая обложка", "price": 30, "stock": 30, "is_active": True},
            {"shop": shop_objects[0], "category": category_objects[3], "name": "Микроволновка Bosch - HMT75M", "slug": "bosch-hmt75m", "description": "Микроволновая печь 20 л, 800 Вт", "price": 300, "stock": 10, "is_active": True},
            {"shop": shop_objects[0], "category": category_objects[5], "name": "Крем L'Oréal - Hydrating", "slug": "loreal-hydrating", "description": "Увлажняющий крем 50 мл, для всех типов кожи", "price": 50, "stock": 40, "is_active": True},
            {"shop": shop_objects[0], "category": category_objects[6], "name": "Конструктор LEGO - Classic 500", "slug": "lego-classic-500", "description": "LEGO Classic, 500 деталей, 6+", "price": 100, "stock": 15, "is_active": True},
            {"shop": shop_objects[0], "category": category_objects[7], "name": "Шоколад Milka - Alpine Milk", "slug": "milka-alpine-milk", "description": "Молочный шоколад 100 г", "price": 5, "stock": 100, "is_active": True},
            {"shop": shop_objects[0], "category": category_objects[4], "name": "Фитнес-браслет Xiaomi - Mi Band 8", "slug": "xiaomi-mi-band-8", "description": "Считает шаги, пульс, водозащита", "price": 80, "stock": 20, "is_active": True},
            {"shop": shop_objects[1], "category": category_objects[0], "name": "Планшет Huawei - MatePad T10", "slug": "huawei-matepad-t10", "description": "Huawei MatePad T10, 64 ГБ, Wi-Fi", "price": 800, "stock": 12, "is_active": True},
            {"shop": shop_objects[1], "category": category_objects[0], "name": "Наушники Sony - WH-CH510", "slug": "sony-wh-ch510", "description": "Беспроводные наушники, Bluetooth", "price": 200, "stock": 25, "is_active": True},
            {"shop": shop_objects[1], "category": category_objects[1], "name": "Футболка Nike - Sportswear", "slug": "nike-sportswear", "description": "Хлопковая футболка, размер L", "price": 40, "stock": 50, "is_active": True},
            {"shop": shop_objects[1], "category": category_objects[1], "name": "Свитер Zara - CozyFit", "slug": "zara-cozyfit", "description": "Тёплый свитер, размер S, wool", "price": 120, "stock": 15, "is_active": True},
            {"shop": shop_objects[1], "category": category_objects[2], "name": "Книга Harper - Dune", "slug": "harper-dune", "description": "Роман Фрэнка Герберта, твёрдая обложка", "price": 35, "stock": 20, "is_active": True},
            {"shop": shop_objects[1], "category": category_objects[3], "name": "Чайник Philips - Daily HD9350", "slug": "philips-hd9350", "description": "Чайник 1.7 л, нержавеющая сталь", "price": 100, "stock": 18, "is_active": True},
            {"shop": shop_objects[1], "category": category_objects[5], "name": "Шампунь Garnier - Fructis", "slug": "garnier-fructis", "description": "Шампунь для волос 250 мл", "price": 20, "stock": 60, "is_active": True},
            {"shop": shop_objects[1], "category": category_objects[6], "name": "Мягкая игрушка Hasbro - Teddy Bear", "slug": "hasbro-teddy-bear", "description": "Плюшевый медведь 30 см", "price": 50, "stock": 30, "is_active": True},
            {"shop": shop_objects[1], "category": category_objects[7], "name": "Кофе Nescafé - Gold", "slug": "nescafe-gold", "description": "Растворимый кофе 100 г", "price": 15, "stock": 80, "is_active": True},
            {"shop": shop_objects[1], "category": category_objects[4], "name": "Коврик Reebok - Yoga Mat 6mm", "slug": "reebok-yoga-mat", "description": "Коврик для йоги 6 мм", "price": 60, "stock": 25, "is_active": True},
            {"shop": shop_objects[2], "category": category_objects[0], "name": "Телевизор LG - 43UP7800", "slug": "lg-43up7800", "description": "Smart TV 43 дюйма, 4K", "price": 1500, "stock": 10, "is_active": True},
            {"shop": shop_objects[2], "category": category_objects[0], "name": "Мышь Logitech - G Pro Wireless", "slug": "logitech-g-pro", "description": "Игровая мышь, беспроводная", "price": 150, "stock": 30, "is_active": True},
            {"shop": shop_objects[2], "category": category_objects[0], "name": "Клавиатура Razer - Huntsman Mini", "slug": "razer-huntsman-mini", "description": "Механическая клавиатура, RGB", "price": 200, "stock": 20, "is_active": True},
            {"shop": shop_objects[2], "category": category_objects[0], "name": "SSD Samsung - 970 EVO 1TB", "slug": "samsung-970-evo-1tb", "description": "SSD 1 ТБ, NVMe", "price": 300, "stock": 15, "is_active": True},
            {"shop": shop_objects[2], "category": category_objects[0], "name": "Power Bank Anker - PowerCore 10000", "slug": "anker-powercore-10000", "description": "Power Bank 10000 мАч", "price": 80, "stock": 40, "is_active": True},
            {"shop": shop_objects[2], "category": category_objects[0], "name": "Часы Xiaomi - Mi Watch 2", "slug": "xiaomi-mi-watch-2", "description": "Умные часы, AMOLED экран", "price": 250, "stock": 12, "is_active": True},
            {"shop": shop_objects[2], "category": category_objects[0], "name": "Роутер TP-Link - Archer AX50", "slug": "tplink-archer-ax50", "description": "Wi-Fi роутер, AX3000", "price": 120, "stock": 18, "is_active": True},
            {"shop": shop_objects[2], "category": category_objects[0], "name": "Веб-камера Logitech - C920 HD", "slug": "logitech-c920-hd", "description": "Веб-камера Full HD", "price": 100, "stock": 25, "is_active": True},
            {"shop": shop_objects[3], "category": category_objects[2], "name": "Книга Эксмо - Война и мир", "slug": "eksmo-war-and-peace", "description": "Роман Л. Толстого, твёрдая обложка", "price": 50, "stock": 15, "is_active": True},
            {"shop": shop_objects[3], "category": category_objects[2], "name": "Книга Азбука - Преступление и наказание", "slug": "azbuka-crime-and-punishment", "description": "Роман Ф. Достоевского", "price": 40, "stock": 20, "is_active": True},
            {"shop": shop_objects[3], "category": category_objects[2], "name": "Книга Bloomsbury - Гарри Поттер", "slug": "bloomsbury-harry-potter", "description": "Дж. Роулинг, 1 часть", "price": 45, "stock": 25, "is_active": True},
            {"shop": shop_objects[3], "category": category_objects[2], "name": "Книга O’Reilly - Python Programming", "slug": "oreilly-python-programming", "description": "Программирование на Python", "price": 60, "stock": 10, "is_active": True},
            {"shop": shop_objects[3], "category": category_objects[2], "name": "Книга АСТ - Мастер и Маргарита", "slug": "ast-master-and-margarita", "description": "Роман М. Булгакова", "price": 35, "stock": 18, "is_active": True},
            {"shop": shop_objects[3], "category": category_objects[2], "name": "Книга Dorling - Kids Encyclopedia", "slug": "dorling-kids-encyclopedia", "description": "Энциклопедия для детей", "price": 30, "stock": 20, "is_active": True},
            {"shop": shop_objects[4], "category": category_objects[4], "name": "Гантели Adidas - PowerLift 10kg", "slug": "adidas-powerlift-10kg", "description": "Пара гантелей 10 кг", "price": 100, "stock": 15, "is_active": True},
            {"shop": shop_objects[4], "category": category_objects[4], "name": "Велосипед Trek - Marlin 7", "slug": "trek-marlin-7", "description": "Горный велосипед, 26 дюймов", "price": 800, "stock": 5, "is_active": True},
            {"shop": shop_objects[4], "category": category_objects[4], "name": "Форма Under Armour - HeatGear", "slug": "under-armour-heatgear", "description": "Комплект для бега, размер M", "price": 120, "stock": 20, "is_active": True},
            {"shop": shop_objects[4], "category": category_objects[4], "name": "Тренажёр Horizon - Andes 3", "slug": "horizon-andes-3", "description": "Эллиптический тренажёр", "price": 1000, "stock": 3, "is_active": True},
            {"shop": shop_objects[4], "category": category_objects[4], "name": "Мяч Adidas - Starlancer V", "slug": "adidas-starlancer-v", "description": "Футбольный мяч, размер 5", "price": 50, "stock": 30, "is_active": True},
            {"shop": shop_objects[4], "category": category_objects[4], "name": "Рюкзак Puma - Active 20L", "slug": "puma-active-20l", "description": "Спортивный рюкзак 20 л", "price": 80, "stock": 25, "is_active": True},
        ]
        product_objects = []
        for prod in products:
            product_obj = Product.objects.create(**prod)
            product_objects.append(product_obj)

        # 6. Carts and CartItems (для buyer1–buyer5)
        self.stdout.write('Step 6/8: Creating Carts and CartItems')
        carts = [
            {
                "user": buyers[0],
                "items": [
                    {"product": product_objects[0], "quantity": 1},
                    {"product": product_objects[2], "quantity": 2},
                    {"product": product_objects[4], "quantity": 1},
                ]
            },
            {
                "user": buyers[1],
                "items": [
                    {"product": product_objects[10], "quantity": 1},
                    {"product": product_objects[20], "quantity": 1},
                ]
            },
            {
                "user": buyers[2],
                "items": [
                    {"product": product_objects[21], "quantity": 1},
                    {"product": product_objects[22], "quantity": 1},
                    {"product": product_objects[23], "quantity": 2},
                    {"product": product_objects[24], "quantity": 1},
                ]
            },
            {
                "user": buyers[3],
                "items": [
                    {"product": product_objects[28], "quantity": 2},
                ]
            },
            {
                "user": buyers[4],
                "items": [
                    {"product": product_objects[8], "quantity": 10},
                    {"product": product_objects[13], "quantity": 1},
                    {"product": product_objects[25], "quantity": 1},
                    {"product": product_objects[30], "quantity": 1},
                    {"product": product_objects[34], "quantity": 2},
                ]
            },
        ]
        for cart_data in carts:
            cart = Cart.objects.create(user=cart_data["user"])
            for item in cart_data["items"]:
                CartItem.objects.create(
                    cart=cart,
                    product=item["product"],
                    quantity=item["quantity"]
                )

        # 7. Orders and OrderItems (для buyer1–buyer6, 15 заказов)
        self.stdout.write('Step 7/8: Creating Orders and OrderItems')
        orders = [
            {
                "user": buyers[0],
                "shop": shop_objects[0],
                "pickup_point": pp_objects[0],
                "status": "delivered",
                "is_paid": True,
                "created_at": timezone.now() - timedelta(days=13),
                "status_updated_at": timezone.now() - timedelta(days=8),
                "items": [
                    {"product": product_objects[0], "quantity": 1, "price": 1200},
                    {"product": product_objects[2], "quantity": 1, "price": 200},
                ]
            },
            {
                "user": buyers[0],
                "shop": shop_objects[1],
                "pickup_point": pp_objects[1],
                "status": "ready_for_pickup",
                "is_paid": False,
                "created_at": timezone.now() - timedelta(days=8),
                "status_updated_at": timezone.now() - timedelta(days=3),
                "items": [
                    {"product": product_objects[10], "quantity": 1, "price": 800},
                ]
            },
            {
                "user": buyers[0],
                "shop": shop_objects[0],
                "pickup_point": pp_objects[2],
                "status": "pending",
                "is_paid": False,
                "created_at": timezone.now() - timedelta(days=1),
                "status_updated_at": timezone.now() - timedelta(days=1),
                "items": [
                    {"product": product_objects[4], "quantity": 2, "price": 30},
                    {"product": product_objects[8], "quantity": 5, "price": 5},
                ]
            },
            {
                "user": buyers[1],
                "shop": shop_objects[2],
                "pickup_point": pp_objects[3],
                "status": "returned",
                "is_paid": False,
                "created_at": timezone.now() - timedelta(days=12),
                "status_updated_at": timezone.now() - timedelta(days=7),
                "items": [
                    {"product": product_objects[20], "quantity": 1, "price": 1500},
                ]
            },
            {
                "user": buyers[1],
                "shop": shop_objects[1],
                "pickup_point": pp_objects[4],
                "status": "confirmed",
                "is_paid": False,
                "created_at": timezone.now() - timedelta(days=3),
                "status_updated_at": timezone.now() - timedelta(days=2),
                "items": [
                    {"product": product_objects[12], "quantity": 2, "price": 40},
                    {"product": product_objects[13], "quantity": 1, "price": 120},
                ]
            },
            {
                "user": buyers[2],
                "shop": shop_objects[2],
                "pickup_point": pp_objects[5],
                "status": "delivered",
                "is_paid": True,
                "created_at": timezone.now() - timedelta(days=14),
                "status_updated_at": timezone.now() - timedelta(days=9),
                "items": [
                    {"product": product_objects[23], "quantity": 1, "price": 300},
                ]
            },
            {
                "user": buyers[2],
                "shop": shop_objects[2],
                "pickup_point": pp_objects[6],
                "status": "ready_for_pickup",
                "is_paid": False,
                "created_at": timezone.now() - timedelta(days=9),
                "status_updated_at": timezone.now() - timedelta(days=8),
                "items": [
                    {"product": product_objects[21], "quantity": 1, "price": 150},
                    {"product": product_objects[22], "quantity": 1, "price": 200},
                ]
            },
            {
                "user": buyers[2],
                "shop": shop_objects[0],
                "pickup_point": pp_objects[0],
                "status": "shipped",
                "is_paid": False,
                "created_at": timezone.now() - timedelta(days=5),
                "status_updated_at": timezone.now() - timedelta(days=3),
                "items": [
                    {"product": product_objects[9], "quantity": 1, "price": 80},
                ]
            },
            {
                "user": buyers[3],
                "shop": shop_objects[3],
                "pickup_point": pp_objects[7],
                "status": "delivered",
                "is_paid": True,
                "created_at": timezone.now() - timedelta(days=15),
                "status_updated_at": timezone.now() - timedelta(days=10),
                "items": [
                    {"product": product_objects[28], "quantity": 2, "price": 50},
                    {"product": product_objects[29], "quantity": 1, "price": 40},
                ]
            },
            {
                "user": buyers[3],
                "shop": shop_objects[3],
                "pickup_point": pp_objects[8],
                "status": "confirmed",
                "is_paid": False,
                "created_at": timezone.now() - timedelta(days=4),
                "status_updated_at": timezone.now() - timedelta(days=3),
                "items": [
                    {"product": product_objects[30], "quantity": 1, "price": 45},
                ]
            },
            {
                "user": buyers[4],
                "shop": shop_objects[4],
                "pickup_point": pp_objects[9],
                "status": "ready_for_pickup",
                "is_paid": False,
                "created_at": timezone.now() - timedelta(days=11),
                "status_updated_at": timezone.now() - timedelta(days=9),
                "items": [
                    {"product": product_objects[34], "quantity": 1, "price": 100},
                    {"product": product_objects[36], "quantity": 1, "price": 120},
                ]
            },
            {
                "user": buyers[4],
                "shop": shop_objects[0],
                "pickup_point": pp_objects[1],
                "status": "returned",
                "is_paid": False,
                "created_at": timezone.now() - timedelta(days=13),
                "status_updated_at": timezone.now() - timedelta(days=8),
                "items": [
                    {"product": product_objects[7], "quantity": 1, "price": 100},
                ]
            },
            {
                "user": buyers[4],
                "shop": shop_objects[1],
                "pickup_point": pp_objects[2],
                "status": "shipped",
                "is_paid": False,
                "created_at": timezone.now() - timedelta(days=6),
                "status_updated_at": timezone.now() - timedelta(days=4),
                "items": [
                    {"product": product_objects[18], "quantity": 3, "price": 15},
                ]
            },
            {
                "user": buyers[5],
                "shop": shop_objects[4],
                "pickup_point": pp_objects[3],
                "status": "delivered",
                "is_paid": True,
                "created_at": timezone.now() - timedelta(days=16),
                "status_updated_at": timezone.now() - timedelta(days=11),
                "items": [
                    {"product": product_objects[35], "quantity": 1, "price": 800},
                ]
            },
            {
                "user": buyers[5],
                "shop": shop_objects[2],
                "pickup_point": pp_objects[4],
                "status": "pending",
                "is_paid": False,
                "created_at": timezone.now(),
                "status_updated_at": timezone.now(),
                "items": [
                    {"product": product_objects[25], "quantity": 1, "price": 250},
                    {"product": product_objects[27], "quantity": 1, "price": 100},
                ]
            },
        ]
        for order_data in orders:
            total_price = sum(item["price"] * item["quantity"] for item in order_data["items"])
            order = Order.objects.create(
                user=order_data["user"],
                shop=order_data["shop"],
                pickup_point=order_data["pickup_point"],
                total_price=total_price,
                status=order_data["status"],
                is_paid=order_data["is_paid"],
                created_at=order_data["created_at"],
                status_updated_at=order_data["status_updated_at"]
            )
            for item in order_data["items"]:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    quantity=item["quantity"],
                    price=item["price"]
                )

        # 8. Reviews (10 отзывов от buyer1–buyer6 на товары из заказов)
        self.stdout.write('Step 8/8: Creating Reviews')
        reviews = [
            {
                "user": buyers[0],
                "product": product_objects[0],
                "rating": 5,
                "comment": "Отличный смартфон, быстрая доставка, всё работает идеально!",
                "created_at": timezone.now() - timedelta(days=8),
            },
            {
                "user": buyers[0],
                "product": product_objects[4],
                "rating": 4,
                "comment": "Книга в хорошем состоянии, но доставка заняла 2 дня.",
                "created_at": timezone.now() - timedelta(days=1),
            },
            {
                "user": buyers[1],
                "product": product_objects[20],
                "rating": 2,
                "comment": "Телевизор хороший, но пришлось вернуть из-за царапины.",
                "created_at": timezone.now() - timedelta(days=7),
            },
            {
                "user": buyers[1],
                "product": product_objects[12],
                "rating": 3,
                "comment": "Качество нормальное, но размер чуть маловат.",
                "created_at": timezone.now() - timedelta(days=2),
            },
            {
                "user": buyers[2],
                "product": product_objects[23],
                "rating": 5,
                "comment": "SSD очень быстрый, установил за 5 минут, доволен!",
                "created_at": timezone.now() - timedelta(days=9),
            },
            {
                "user": buyers[2],
                "product": product_objects[21],
                "rating": 4,
                "comment": "Мышь удобная, но кнопки немного шумные.",
                "created_at": timezone.now() - timedelta(days=8),
            },
            {
                "user": buyers[3],
                "product": product_objects[28],
                "rating": 5,
                "comment": "Книга в идеальном состоянии, быстро забрал на ПВЗ.",
                "created_at": timezone.now() - timedelta(days=10),
            },
            {
                "user": buyers[3],
                "product": product_objects[30],
                "rating": 4,
                "comment": "Интересная книга, но обложка слегка помята.",
                "created_at": timezone.now() - timedelta(days=3),
            },
            {
                "user": buyers[4],
                "product": product_objects[34],
                "rating": 3,
                "comment": "Гантели хорошие, но ждал на ПВЗ дольше обычного.",
                "created_at": timezone.now() - timedelta(days=9),
            },
            {
                "user": buyers[5],
                "product": product_objects[35],
                "rating": 5,
                "comment": "Велосипед превзошёл ожидания, отличное качество!",
                "created_at": timezone.now() - timedelta(days=11),
            },
        ]
        for review_data in reviews:
            Review.objects.create(
                user=review_data["user"],
                product=review_data["product"],
                rating=review_data["rating"],
                comment=review_data["comment"],
                created_at=review_data["created_at"]
            )

        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully!'))
