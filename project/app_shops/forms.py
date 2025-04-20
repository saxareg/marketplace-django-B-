from django import forms
from models import Shop


class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['name', 'slug', 'description', 'logo', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'name': 'Название магазина',
            'slug': 'URL-идентификатор',
            'description': 'Описание',
            'logo': 'Логотип',
            'is_active': 'Активен',
        }
