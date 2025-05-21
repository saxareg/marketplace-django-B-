from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import *
from app_orders.models import Order
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST


def register(request):
    """Handle user registration.
    On POST: validate and create a new user and associated profile, then log the user in.
    On GET: display the registration form.
    Returns:
        HTTP response with registration form or redirect to 'products' on success.
    """

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = UserProfile(user=user)
            profile.save()
            login(request, user)
            return redirect('products')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    """Handle user login.
    On POST: validate login form and authenticate user.
    On GET: display the login form.
    Returns:
        HTTP response with login form or redirect to 'products' on success.
    """

    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('products')
    else:
        form = UserLoginForm()

    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    """Log out the current user and redirect to 'products' page."""

    logout(request)
    return redirect('products')


@login_required
def profile_view(request):
    """
    Display and update the profile page for the logged-in user.
    Supports updating user info (username, email) and phone number via separate forms.
    Returns:
        HTTP response rendering profile page with user forms.
    """

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
                return redirect('me')

        elif form_type == 'phone_form':
            phone_form = PhoneForm(request.POST, instance=user_profile)
            if phone_form.is_valid():
                phone_form.save()
                return redirect('me')

    return render(request, 'users/profile.html', {
        'user_form': user_form,
        'phone_form': phone_form,
        'user_profile': user_profile,
    })


@login_required
@require_POST
def switch_role(request):
    """
    Switch the role of the logged-in user between 'buyer' and 'seller'.
    If the user role is neither buyer nor seller (e.g. 'admin' or 'pp_staff'),
    switching is forbidden.
    Returns:
        JsonResponse with new role on success or HttpResponseForbidden if switching is not allowed.
    """

    userprofile = request.user.profile

    if userprofile.role == 'buyer':
        userprofile.role = 'seller'
    elif userprofile.role == 'seller':
        userprofile.role = 'buyer'
    else:
        return HttpResponseForbidden("Role switching is not allowed")

    userprofile.save()
    return JsonResponse({'status': 'ok', 'new_role': userprofile.role})


@login_required
def pp_view(request):
    """
    Display orders for the pickup point associated with the logged-in pickup point staff.
    Orders are sorted by creation date in descending order.
    Returns:
        HTTP response rendering the pickup point orders page.
    """

    profile = request.user.profile
    orders = Order.objects.filter(pickup_point=profile.pickup_point).order_by('-created_at')

    return render(request, 'users/pp.html', {
        'orders': orders,
        'pickup_point': profile.pickup_point,
    })


def custom_404(request, exception):
    """Custom 404 error handler.
    Returns:
        HTTP response rendering custom 404 page with status 404.
    """

    return render(request, '404.html', status=404)
