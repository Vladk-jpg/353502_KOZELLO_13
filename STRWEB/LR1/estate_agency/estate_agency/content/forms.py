from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.NumberInput(attrs={
                'min': '1',
                'max': '10',
                'placeholder': 'Оценка от 1 до 10'
            }),
            'text': forms.Textarea(attrs={
                'rows': '4',
                'placeholder': 'Ваш отзыв'
            })
        } 