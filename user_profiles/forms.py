from django import forms
from .models import UserBookList


class UserBookListForm(forms.ModelForm):
    """Form for managing user's book lists"""
    
    class Meta:
        model = UserBookList
        fields = ['is_favorite', 'is_read', 'notes']
        widgets = {
            'is_favorite': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'id_is_favorite'
            }),
            'is_read': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'id_is_read'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Add personal notes about this book...'
            })
        }


class QuickToggleForm(forms.Form):
    """Simple form for quick toggle actions via AJAX"""
    action = forms.ChoiceField(choices=[
        ('toggle_favorite', 'Toggle Favorite'),
        ('toggle_read', 'Toggle Read Status'),
    ])
    book_id = forms.IntegerField(widget=forms.HiddenInput())