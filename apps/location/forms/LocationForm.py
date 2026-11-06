# forms.py
from django import forms
from django.forms import DateTimeInput
from apps.location.models import DossierLocation


class DossierLocationForm(forms.ModelForm):
    class Meta:
        model = DossierLocation
        exclude = (
            "client",
            "vehicule",
            "code_location",
            "status",
            "yousign_request_id",
            "yousign_document_id",
            "contrat_pdf",
            "signed_contract_pdf",
            "date_creation",
            "deal",
            "message",
            "mysignature"
        )

        widgets = {
            "nom_complet": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nom et prénom"
            }),
            "telephone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Téléphone"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Email"
            }),
            "adresse": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Adresse complète"
            }),
            "numero_permis": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Numéro du permis"
            }),
            "pays_delivrance_permis": forms.Select(attrs={
                "class": "form-select"
            }),
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
            "lieu_depart": forms.Select(attrs={
                "class": "form-select"
            }),
            "lieu_retour": forms.Select(attrs={
                "class": "form-select"
            }),
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
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Format attendu par datetime-local
        self.fields["date_depart"].input_formats = [
            "%Y-%m-%dT%H:%M"
        ]
        self.fields["date_retour"].input_formats = [
            "%Y-%m-%dT%H:%M"
        ]