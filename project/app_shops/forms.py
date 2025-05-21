from django import forms
from django.utils.text import slugify
from .models import Shop, ShopCreationRequest


class BaseShopForm(forms.ModelForm):
    """
    Base form for shop-related models.
    Handles shared fields and validation logic such as slug normalization.
    """

    class Meta:
        fields = ['name', 'slug', 'description', 'logo']
        widgets = {'description': forms.Textarea(attrs={'rows': 4})}
        labels = {
            'name': 'Название магазина',
            'slug': 'URL-идентификатор',
            'description': 'Описание магазина',
            'logo': 'Логотип',
        }

    def clean_slug(self):
        """
        Normalize the slug using `slugify`.
        Raise ValidationError if the result is empty.
        """

        slug = self.cleaned_data['slug']
        normalized_slug = slugify(slug)
        if not normalized_slug:
            raise forms.ValidationError("Слаг должен содержать только латинские буквы, цифры и дефисы.")
        return normalized_slug


class ShopForm(BaseShopForm):
    """
    Form for editing or creating an active shop.
    Inherits base validation and adds a check for slug uniqueness in the Shop model.
    """

    class Meta(BaseShopForm.Meta):
        model = Shop
        fields = BaseShopForm.Meta.fields + ['is_active']

    def clean_slug(self):
        """Ensure the slug is unique among existing Shop instances."""

        slug = super().clean_slug()
        if Shop.objects.filter(slug=slug).exists():
            raise forms.ValidationError("Такой URL-идентификатор уже используется. Пожалуйста, выберите другой.")
        return slug


class ShopCreationRequestForm(BaseShopForm):
    """
    Form for users to submit a request to create a new shop.
    Checks slug uniqueness in ShopCreationRequest model.
    """

    class Meta(BaseShopForm.Meta):
        model = ShopCreationRequest
        fields = BaseShopForm.Meta.fields

    def clean_slug(self):
        """Ensure the slug is unique among ShopCreationRequest instances."""

        slug = super().clean_slug()
        if ShopCreationRequest.objects.filter(slug=slug).exists():
            raise forms.ValidationError("Этот URL-идентификатор уже занят.")
        return slug
