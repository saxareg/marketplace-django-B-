from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages


# Представление для регистрации
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация прошла успешно!")
            return redirect('home')  # Перенаправление на главную страницу
        else:
            messages.error(request, "Ошибка при регистрации.")
    else:
        form = UserCreationForm()

    return render(request, 'users/register.html', {'form': form})


# Представление для входа
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Неверные данные для входа.")
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})


# Представление для выхода
def logout_view(request):
    logout(request)
    return redirect('products')
