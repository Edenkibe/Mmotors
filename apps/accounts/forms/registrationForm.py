from django import forms
from django.contrib.auth.forms import UserCreationForm
from ..models import User
from django.core.exceptions import ValidationError
import re

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'password',)
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control rounded-left',
        'placeholder': 'Username'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control rounded-left',
        'placeholder': 'Email'
    }))
    password= forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control rounded-left',
        'id': 'myInput',
        'type': 'password',
        'placeholder': 'Mot de passe'
    }))
   
        # Custom validation using regex
    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.match(r'[A-Za-z0-9_ ]{3,20}+$', username):
            raise ValidationError(
                "Username must be 3-20 characters long and contain only letters, numbers, or underscores. and space"
            )
        
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username already exists.")

        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        # simple regex for email (optional because EmailField already validates)
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            raise ValidationError("Enter a valid email address.")
        
    
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email already exists.")    
        
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)

        # hash  le mot de passe avant de le sauvegarder
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()

        return user
    
class admin_register_userForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'role')
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control rounded-left',
        'placeholder': 'Username'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control rounded-left',
        'placeholder': 'Email'
    }))
    password= forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control rounded-left',
        'id': 'myInput',
        'type': 'password',
        'placeholder': 'Mot de passe'
    }))
    role = forms.ChoiceField(choices=User.role_choise, widget=forms.Select(attrs={
        'class': 'form-control rounded-left',
        'placeholder': 'Role'
    }))

        # Custom validation using regex
    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.match(r'[A-Za-z0-9_ ]{3,20}+$', username):
            raise ValidationError(
                "Username must be 3-20 characters long and contain only letters, numbers, or underscores. and space"
            )
        
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username already exists.")

        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        # simple regex for email (optional because EmailField already validates)
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            raise ValidationError("Enter a valid email address.")
        
    
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email already exists.")    
        
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)

        # hash  le mot de passe avant de le sauvegarder
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()

        return user    