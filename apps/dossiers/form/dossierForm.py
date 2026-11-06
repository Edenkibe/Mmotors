from django import forms
import re
from django.core.exceptions import ValidationError
import uuid
from apps.dossiers.models import DossierAchat
import os


def child_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f'children/{instance.user.username}/{instance.name}/{filename}'

class DossierAchatForm(forms.ModelForm):

    class Meta:
        model = DossierAchat
        fields = ['nom_complet', 'telephone','adresse','email','piece_identite']

    
        widgets = {
            "nom_complet": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex : Jean Dupont"
            }),

            "adresse": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex : 12 rue Charles du Bois"
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Email"
            }),

            "telephone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex : +33612345678"
            }),

            "piece_identite": forms.ClearableFileInput(attrs={
                "class": "form-control",
                "accept": ".pdf,.doc,.docx"
            }),
        }
   #this function init handle the user keywords
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    # Custom regex validator for field here:
    def clean_nom_complet(self):
        nom_complet = self.cleaned_data.get('nom_complet')
        pattern =r"^[A-Za-zÀ-ÖØ-öø-ÿ' -]{2,50}$"
        if not re.match(pattern, nom_complet):
            raise ValidationError("Fullname can only contain letters and spaces and min letter 2.")
        return nom_complet
    

    def clean_adresse(self):
        adresse = self.cleaned_data.get('adresse')
        pattern = r'^[a-zA-Z-0-9.,\-\/\s]{2,100}$'
        if not re.match(pattern, adresse):
            raise ValidationError("the adresse has to like ex: 12 rue,boire etc")
        return adresse
    
    def clean_email(self):
        email = self.cleaned_data['email']
        # simple regex for email (optional because EmailField already validates)
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            raise ValidationError("Enter a valid email address.")
        return email
    
    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        pattern = r'^\+?[0-9]{8,15}$'
        if not re.match(pattern, telephone):
            raise ValidationError("your contact number as to be like 06...,+33... or 0033...")
        return telephone
    
    def clean_piece_identite(self):
        piece_identite = self.cleaned_data.get("piece_identite")

        if piece_identite:
            # Maximum size: 5 MB
            max_size = 5 * 1024 * 1024
            if piece_identite.size > max_size:
                raise ValidationError("Document size must be under 5 MB.")

            # Allowed extensions
            allowed_extensions = [".pdf", ".doc", ".docx"]
            ext = os.path.splitext(piece_identite.name)[1].lower()

            if ext not in allowed_extensions:
                raise ValidationError(
                    f"Unsupported file format. Allowed formats: {', '.join(allowed_extensions)}"
                )

            # Optional: Validate MIME type
            allowed_mime_types = [
                "application/pdf",
                "application/msword",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ]

            if hasattr(piece_identite, "content_type"):
                if piece_identite.content_type not in allowed_mime_types:
                    raise ValidationError("Invalid document type.")

        return piece_identite
        
    
        

