from django import forms
from .models import PlatformComment

class PlatformCommentForm(forms.ModelForm):
    class Meta:
        model=PlatformComment
        fields=['comment']
        