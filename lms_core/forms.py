from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }