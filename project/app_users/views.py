from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import *


# Представление для регистрации
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('products')  # Перенаправление на главную страницу
        else:
            messages.error(request, "Ошибка при регистрации.")
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


# Представление для входа
def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('products')
        else:
            messages.error(request, "Неверные данные для входа.")
    else:
        form = UserLoginForm()

    return render(request, 'users/login.html', {'form': form})


# Представление для выхода
def logout_view(request):
    logout(request)
    return redirect('products')
