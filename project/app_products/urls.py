from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='products'),
    path('create/', views.create_product, name='create_product'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),
    path('<slug:slug>/delete/', views.delete_product, name='delete_product'),
    path('<slug:slug>/edit/', views.edit_product, name='edit_product'),
    path('<slug:slug>/add-review/', views.add_review, name='add-review'),
]
