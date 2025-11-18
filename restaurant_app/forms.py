from django import forms
from .models import Review, Order
from django.contrib.auth import get_user_model

User = get_user_model()

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'rating': forms.Select(attrs={'class': 'form-select'}),
        }

class OrderCreateForm(forms.ModelForm):
    email = forms.EmailField(label="Електронна пошта", 
        widget=forms.EmailInput(attrs={'class': 'form-control'}))

    PAYMENT_CHOICES = [
        ('cash', 'Готівка при отриманні'),
        ('online', 'Онлайн оплата (тимчасово недоступна)'),
    ]
    
    payment_method = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        widget=forms.RadioSelect,
        initial='cash',
        label='Спосіб оплати'
    )

    comment = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3}),
        label='Коментар до замовлення'
    )

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'address', 'payment_method', 'comment']
        labels = {
            'first_name': "Ім'я",
            'last_name': "Прізвище",
            'phone_number': "Номер телефону",
            'email': "Електронна пошта",
            'address': "Адреса доставки",
        }
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['first_name', 'last_name', 'phone_number', 'address', 'comment', 'email']:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

class UserProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(label="Ім'я", max_length=150)
    last_name = forms.CharField(label="Прізвище", max_length=150)
    email = forms.EmailField(label="Електронна пошта")

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})