from django import forms
from .models import Order
from app_users.models import PickupPoints


class OrderCreateForm(forms.ModelForm):
    pickup_point = forms.ModelChoiceField(
        queryset=PickupPoints.objects.all(),
        required=True,
        label='Пункт выдачи',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Order
        fields = ['pickup_point']
