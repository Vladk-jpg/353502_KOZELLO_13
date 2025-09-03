from django import forms
from .models import Property
from sales.models import Promo

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'description', 'price', 'category', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'price': forms.NumberInput(attrs={'min': 0}),
        }

class ReservationForm(forms.Form):
    promo_code = forms.CharField(
        max_length=50,
        required=False,
        label='Промокод',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    ) 