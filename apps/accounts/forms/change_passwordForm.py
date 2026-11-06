from django import forms
from ..models import User
from django.core.exceptions import ValidationError
import re

class ChangePasswordForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'password',)
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control ',
        'type': 'password',
        'id': 'myInput',
        'placeholder': 'Ancien mot de passe'
    }))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control ',
        'type': 'password',
        'id': 'myInput',
        'placeholder': 'Nouveau mot de passe'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'type': 'password',
        'id': 'myInput',
        'placeholder': 'Confirmer le mot de passe'
    }))
   