# forms.py
from django import forms
from django.forms import DateTimeInput

from apps.location.models import DossierLocation


class DossierLocationForm(forms.ModelForm):
    class Meta:
        model = DossierLocation
        fields = [
            "nom_complet",
            "telephone",
            "email",
            "adresse",
            "numero_permis",
            "pays_delivrance_permis",
            "date_depart",
            "date_retour",
            "lieu_depart",
            "lieu_retour",
            "autre_lieu_depart",
            "autre_lieu_retour",
        ]
        widgets = {
            "nom_complet": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nom et prénom"}
            ),
            "telephone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Téléphone"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Email"}
            ),
            "adresse": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Adresse complète"}
            ),
            "numero_permis": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Numéro du permis"}
            ),
            "pays_delivrance_permis": forms.Select(attrs={"class": "form-select"}),
            "date_depart": DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                },
                format="%Y-%m-%dT%H:%M",
            ),
            "date_retour": DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                },
                format="%Y-%m-%dT%H:%M",
            ),
            "lieu_depart": forms.Select(attrs={"class": "form-select"}),
            "lieu_retour": forms.Select(attrs={"class": "form-select"}),
            # Nouveaux champs
            "autre_lieu_depart": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Précisez l'adresse de départ",
                }
            ),
            "autre_lieu_retour": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Précisez l'adresse de retour",
                }
            ),
        }
        labels = {
            "nom_complet": "Nom et prénom",
            "telephone": "Téléphone",
            "email": "Email",
            "adresse": "Adresse complète",
            "numero_permis": "Numéro du permis de conduire",
            "pays_delivrance_permis": "Pays de délivrance du permis",
            "date_depart": "Date et heure de départ",
            "date_retour": "Date et heure de retour",
            "lieu_depart": "Lieu de prise en charge",
            "lieu_retour": "Lieu de restitution",
            # Nouveaux labels
            "autre_lieu_depart": "Adresse personnalisée du départ",
            "autre_lieu_retour": "Adresse personnalisée du retour",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Format attendu par datetime-local
        self.fields["date_depart"].input_formats = ["%Y-%m-%dT%H:%M"]
        self.fields["date_retour"].input_formats = ["%Y-%m-%dT%H:%M"]

    # il verifie que le client ne peut pas choisir "Autre" sans remplir le champ correspondant:
    def clean(self):
        cleaned_data = super().clean()

        lieu_depart = cleaned_data.get("lieu_depart")
        lieu_retour = cleaned_data.get("lieu_retour")

        autre_lieu_depart = cleaned_data.get("autre_lieu_depart")
        autre_lieu_retour = cleaned_data.get("autre_lieu_retour")

        if lieu_depart == "Autre" and not (autre_lieu_depart or "").strip():
            self.add_error(
                "autre_lieu_depart", "Veuillez préciser l'adresse de départ."
            )

        if lieu_retour == "Autre" and not (autre_lieu_retour or "").strip():
            self.add_error(
                "autre_lieu_retour", "Veuillez préciser l'adresse de retour."
            )

        return cleaned_data
