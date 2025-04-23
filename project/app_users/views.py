from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import *


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = UserProfile(user=user)
            profile.save()
            login(request, user)
            return redirect('products')
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


@login_required
def profile_view(request):
    user = request.user
    user_profile = user.profile

    user_form = UserProfileUpdateForm(instance=user)
    phone_form = PhoneForm(instance=user_profile)

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'user_form':
            user_form = UserProfileUpdateForm(request.POST, instance=user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Данные обновлены.')
                return redirect('me')

        elif form_type == 'phone_form':
            phone_form = PhoneForm(request.POST, instance=user_profile)
            if phone_form.is_valid():
                phone_form.save()
                messages.success(request, 'Номер телефона обновлен.')
                return redirect('me')

    return render(request, 'users/profile.html', {
        'user_form': user_form,
        'phone_form': phone_form,
        'user_profile': user_profile
    })

