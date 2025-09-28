from django import forms
from .models import Review, Order

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'phone_number', 'address', 'payment_method']
        widgets = {
            'payment_method': forms.RadioSelect,
        }