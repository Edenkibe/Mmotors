from django import forms
from ..models import User
from django.core.exceptions import ValidationError
import re

class InfoModificationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name')
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Last Name'
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'First Name'
    }))

        # Custom validation using regex
    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.match(r'^[A-Za-z0-9_ ]{3,20}+$', username):
            raise ValidationError(
                "Username must be 3-20 characters long and contain only letters, numbers, or underscores and space."
            )
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not re.match(r'^[A-Za-z0-9_ ]{3,20}+$', first_name):
            raise ValidationError(
                "First name must be 3-20 characters long and contain only letters, numbers, or underscores and space."
            )
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not re.match(r'^[A-Za-z0-9_ ]{3,20}+$', last_name):
            raise ValidationError(
                "Last name must be 3-20 characters long and contain only letters, numbers, or underscores and space."
            )
        return last_name
    
