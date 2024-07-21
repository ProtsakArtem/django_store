from django import forms
from orders.models import Order


class OrderForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Тарас"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Шевченко"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "+380000000000"}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Полтава, 8 відділення"}))
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'address']
