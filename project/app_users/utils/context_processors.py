from app_orders.models import CartItem


def user_profile(request):
    if request.user.is_authenticated:
        return {'userprofile': request.user.profile}
    return {'userprofile': None}


def cart_item_count(request):
    count = 0
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(cart__user=request.user)
        count = sum(item.quantity for item in cart_items)
    return {'cart_item_count': count}