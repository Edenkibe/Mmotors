from django import forms
from django.core.exceptions import ValidationError
from apps.dossiers.models import DossierAchat



class ReplydossierForm(forms.ModelForm):

    class Meta:
        model = DossierAchat
        fields = ['verification','message']
        
   
        widgets = {
            "verification": forms.Select(attrs={
                "class": "form-select",
            }),
            "message": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "your message",
                "rows": 5
            }),
        }
   
    
        

