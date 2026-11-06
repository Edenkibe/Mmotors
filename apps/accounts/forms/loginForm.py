from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        
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
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox()) 
