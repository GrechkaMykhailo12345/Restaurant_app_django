from django import forms
from .models import Review, Order

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }

class OrderCreateForm(forms.ModelForm):
    full_name = forms.CharField(max_length=100, label="Повне ім'я (Ім'я та Прізвище)", 
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
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
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['phone_number']:
             self.fields[field_name].widget.attrs.update({'class': 'form-control'})