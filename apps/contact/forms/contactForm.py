from django import forms
from apps.contact.models import ContactDossier
from apps.dossiers.models import DossierAchat
from apps.location.models import DossierLocation


class ContactDossierForm(forms.ModelForm):

    class Meta:
        model = ContactDossier
        fields = [
            "nom",
            "email",
            "code_dossier",
            "type",
            "message"
        ]
        
        widgets = {
            "nom": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "your names Ex : Jean Dupont"
            }),
        
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Email"
            }),
        
            "code_dossier": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "your coder :ML5PLOS8MP"
            }),
            "type": forms.Select(attrs={
                "class": "form-select",
            }),
        
            "message": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "your message",
                "rows": 5
            }),
        }    

    def clean_code_dossier(self):
        code = self.cleaned_data["code_dossier"]

        dossier_achat = DossierAchat.objects.filter(
        code_dossier=code
        ).exists()

        dossier_location = DossierLocation.objects.filter(
            code_location=code
        ).exists()

        if not dossier_achat and not dossier_location:
            raise forms.ValidationError(
                "Ce numéro de dossier n'existe pas."
            )

        return code