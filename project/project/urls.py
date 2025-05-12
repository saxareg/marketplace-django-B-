from django.shortcuts import redirect
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('products/', include('app_products.urls')),
    path('users/', include('app_users.urls')),
    path('cart/', include('app_orders.urls')),
    path('shops/', include('app_shops.urls')),
    path('custom_admin/', include('app_admin.urls')),  # Кастомная админка
    path('', lambda request: redirect('products/')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
