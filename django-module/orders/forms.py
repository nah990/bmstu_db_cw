from django import forms

from orders.models import Order


class OrderForm(forms.ModelForm):
    product_name = forms.CharField(label="Ticket", widget=forms.TextInput(attrs={'class': 'form-control order'}))
    min_price = forms.IntegerField(label="Min Price", widget=forms.TextInput(attrs={'class': 'form-control order'}))
    price = forms.IntegerField(label="Average Price", widget=forms.TextInput(attrs={'class': 'form-control order'}))
    max_price = forms.IntegerField(label="Max Price", widget=forms.TextInput(attrs={'class': 'form-control order'}))
    created_time = forms.DateTimeField(label="Date", widget=forms.TextInput(
        attrs={'class': 'form-control order', 'placeholder': 'YY-mm-dd H:i:s'}))

    class Meta:
        model = Order
        fields = ['product_name', 'min_price', 'price', 'max_price', 'created_time']
