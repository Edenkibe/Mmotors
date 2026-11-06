from django.forms import inlineformset_factory
from apps.promotion.models import Promotion
from django import forms


class promotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = [
            "titre",
            "description",
            "start_date",
            "end_date",
        ]

        widgets = {
            "titre": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex : Pour la vie"
            }),

            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Décrivez votre véhicule..."
            }),

           'start_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),

            'end_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            
        }

        labels = {
            "titre": "titre",
            "description": "Description",
            "start_date": "start_date",
            "end_date": "end_date",
        }

#modifier form promo
class Promo_modificationForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = [
            "titre",
            "description",
            "start_date",
            "end_date",
            "disponibilite"
        ]

        widgets = {
            "titre": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex : Pour la vie"
            }),

            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Décrivez votre véhicule..."
            }),

           'start_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),

            'end_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            
            "disponibilite": forms.Select(attrs={
                "class": "form-select"
            }),
        }

        labels = {
            "titre": "titre",
            "description": "Description",
            "start_date": "start_date",
            "end_date": "end_date",
            "disponibilite": "disponibilite",
        }
   