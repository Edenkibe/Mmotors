from django import forms

from apps.location.models import DossierLocation


class Reply_locatioForm(forms.ModelForm):

    class Meta:
        model = DossierLocation
        fields = ['status','message']

        widgets = {
            "status": forms.Select(attrs={
                "class": "form-select",
            }),
            "message": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "your message",
                "rows": 5
            }),
        }




