from django import forms
from .models import BookRating, BookReview


class BookRatingForm(forms.ModelForm):
    class Meta:
        model = BookRating
        fields = ('score',)
        widgets = {
            'score': forms.NumberInput(attrs={
                'min': 1,
                'max': 5,
                'class': 'form-control',
                'placeholder': 'Rate from 1 to 5 stars'
            })
        }
        labels = {
            'score': 'Rating'
        }


class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ('review',)
        widgets = {
            'review': forms.Textarea(attrs={
                'rows': 5,
                'cols': 50,
                'placeholder': 'Write your review here...',
                'class': 'form-control'
            })
        }
        labels = {
            'review': 'Your Review'
        }
