from django.forms import inlineformset_factory
from apps.voiture.models import Photo, Voiture
from django import forms


class VoitureForm(forms.ModelForm):
    class Meta:
        model = Voiture
        fields = [
            "marque",
            "modele",
            "annee",
            "prix",
            "type",
            "carburant",
            "boite",
            "kilometre",
            "etat",
            "description",
        ]

        widgets = {
            "marque": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex : Peugeot"
            }),

            "modele": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex : 308 GT"
            }),

            "annee": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 1950,
                "placeholder": "Ex : 1950"
            }),

            "prix": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
                "placeholder": "15000"
            }),
            "type": forms.Select(attrs={
                 "class": "form-select"
            }),
            "carburant": forms.Select(attrs={
                "class": "form-select"
            }),

            "boite": forms.Select(attrs={
                "class": "form-select"
            }),

            "kilometre": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 0
            }),

            "etat": forms.Select(attrs={
                "class": "form-select"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Décrivez votre véhicule..."
            }),
        }

        labels = {
            "marque": "Marque",
            "modele": "Modèle",
            "annee": "Année",
            "prix": "Prix (€)",
            "type": "Type de transaction",
            "carburant": "Carburant",
            "boite": "Boîte de vitesse",
            "kilometre": "Kilométrage",
            "etat": "État",
            "description": "Description",
        }

    def clean_annee(self):
        annee = self.cleaned_data["annee"]

        from datetime import datetime

        current_year = datetime.now().year

        if annee < 1950 or annee > current_year + 1:
            raise forms.ValidationError("Année invalide.")

        return annee

    def clean_prix(self):
        prix = self.cleaned_data["prix"]

        if prix <= 0:
            raise forms.ValidationError("Le prix doit être supérieur à 0.")

        return prix

    def clean_kilometre(self):
        km = self.cleaned_data["kilometre"]

        if km < 0:
            raise forms.ValidationError("Le kilométrage ne peut pas être négatif.")

        return km
    
    
    
class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = [
            "image",
            "is_main",
        ]
        widgets = {
            "image": forms.FileInput(attrs={
                "class": "form-control"
            }),
            
            'is_main': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

        labels = {
            'image': 'Photo',
            'is_main': 'Photo principale',
        }
    
class typeForm(forms.ModelForm):
    class Meta:
        model = Voiture
        fields = [
            "prix",
            "type",           
        ]

        widgets = {
            "prix": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
                "placeholder": "15000"
            }),
            "type": forms.Select(attrs={
                 "class": "form-select"
            }),
           
        }

        labels = {
            "prix": "Prix (€)",
            "type": "Type de transaction",
        }
    