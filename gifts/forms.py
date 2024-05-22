from django import forms
from .models import GiftBook

class BookForm(forms.ModelForm):
    class Meta:
        model=GiftBook
        fields='__all__'
