from django import forms
from .models import Profile

# CITE: https://docs.djangoproject.com/en/3.2/topics/forms/
class EditProfileForm(forms.ModelForm):
    # username = forms.CharField(label='Username:', max_length=50)
    class Meta:
        model = Profile
        fields = ('username', 'pfp', 'bio')
        widgets = {
            'username': forms.TextInput(attrs={
                'class':'edit_username'
            }),
            
        }