from django import forms
from .models import Product, Review, Category


class ProductForm(forms.ModelForm):
    """
    Form for creating or updating Product instances.
    Applies consistent Bootstrap styling and customizes file input labels.
    """

    class Meta:
        model = Product
        fields = ['category', 'name', 'slug', 'description', 'price', 'stock', 'image']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        """
        Initializes the form with custom widget attributes.
        Sets Bootstrap classes and tweaks file input labels.
        """

        super(ProductForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.ClearableFileInput):
                field.widget.clear_checkbox_label = ''  # пустая надпись для чекбокса
                field.widget.initial_text = 'Текущее'  # убрать надпись "Currently"
                field.widget.input_text = 'Загрузить новое'  # можно поменять подпись
                field.widget.clear_checkbox_label = None
            field.widget.attrs.update({'class': 'form-control'})


class ReviewForm(forms.ModelForm):
    """
    Form for submitting a product review.
    Includes a 1-5 star rating and an optional comment.
    """

    rating = forms.ChoiceField(
        choices=[(i, f'{i} ⭐') for i in range(1, 6)],
        label="Оценка",
        widget=forms.RadioSelect
    )
    comment = forms.CharField(
        label="Комментарий",
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False
    )

    class Meta:
        model = Review
        fields = ['rating', 'comment']


class CategoryForm(forms.ModelForm):
    """
    Form for creating or editing a product category.
    Includes name, slug, and optional description with custom labels and layout.
    """

    class Meta:
        model = Category
        fields = ['name', 'slug', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'name': 'Название',
            'slug': 'URL-идентификатор',
            'description': 'Описание (необязательно)',
        }
