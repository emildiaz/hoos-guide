from django import forms
from .models import Review

# CITE: https://docs.djangoproject.com/en/3.2/topics/forms/
class ReviewForm(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'Write review...',
            'rows': 2,
            'cols': 30,
        }
    ))
    class Meta:
        model = Review
        fields = ('content',)