from django import forms
from .models import Order, CartItem
from app_users.models import PickupPoints


class CartItemForm(forms.ModelForm):
    """
    Form for editing a cart item.
    Allows the user to select a product and specify its quantity.
    """

    class Meta:
        model = CartItem
        fields = ['product', 'quantity']


class OrderStatusUpdateForm(forms.ModelForm):
    """
    Admin form for updating the status of an order.
    Only allows specific status choices: Ready for pickup, Delivered, or Returned.
    """

    class Meta:
        model = Order
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        """
        Initializes the form with a restricted list of allowed order statuses.
        This prevents setting arbitrary statuses from the admin interface.
        """

        super().__init__(*args, **kwargs)
        allowed_statuses = [
            ('ready_for_pickup', 'Ready for pickup'),
            ('delivered', 'Delivered'),
            ('returned', 'Returned')
        ]
        self.fields['status'].choices = allowed_statuses


class OrderCreate(forms.Form):
    """
    Form for placing an order.
    Allows the customer to select a payment method and a pickup point.
    """

    payment_method = forms.ChoiceField(
        choices=[('online', 'Online'), ('offline', 'Offline')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
        error_messages={'required': ''},
    )

    pickup_point = forms.ModelChoiceField(
        queryset=PickupPoints.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
        error_messages={'required': ''},
    )
