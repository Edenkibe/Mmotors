import secrets
import string
from django.db import models
import uuid
from apps.accounts.models import User
from apps.voiture.models import Voiture

#url du generated pdf
def pdf_location_contrat_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f' contrat_location/{instance.client.first_name}/{instance.client.last_name}-{instance.vehicule.marque}/{filename}'

#url du signed contrat pdf pdf:
def signed_location_contrat_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f' signed_location/{instance.client.first_name}/{instance.client.last_name}-{instance.vehicule.marque}/{filename}'

#url du invoice
def facture_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f' invoice/{instance.client.first_name}/{instance.client.last_name}-{instance.vehicule.marque}/{filename}'

class DossierLocation(models.Model):
 
    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="dossiers_location_users"
    )

    vehicule = models.ForeignKey(
        Voiture,
        on_delete=models.CASCADE,
        related_name="dossiers_location_voitures"
    )

    # Informations personnelles
    nom_complet = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)
    email = models.EmailField()
    adresse = models.CharField(max_length=255)

    # Documents
    numero_permis = models.CharField(max_length=40)
    pays_choise= [
        ('France', 'France'),
        ('Belgique', 'Belgique'),
        ('Suisse', 'Suisse'),
        ('Luxembourg', 'Luxembourg'),
        ('Allemagne', 'Allemagne'),
        ('Italie', 'Italie'),
        ('Espagne', 'Espagne'),
        ('Portugal', 'Portugal'),
        ('Pays-Bas', 'Pays-Bas'),
        ('Autre', 'Autre'),
    ]
    pays_delivrance_permis = models.CharField(
        max_length=20,
        choices=pays_choise,
        default='France'
    )
    message = models.TextField( blank=True,null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_depart = models.DateTimeField()
    date_retour = models.DateTimeField()
    
    lieu_prise_en_charge_choix= [
        ('Aéroport saint exupery', 'Aéroport saint exupery'),
        ('Gare part dieu', 'Gare part dieu'),
        ('Gare perrache', 'Gare perrache'),
        ('Hôtel ibis lyon 7', 'Hôtel ibis lyon 7'),
        ('place Bellecour', 'place Bellecour'),
        ('Autre', 'Autre'),
    ]
    lieu_du_retour_choix= [
            ('Aéroport saint exupery', 'Aéroport saint exupery'),
            ('Gare part dieu', 'Gare part dieu'),
            ('Gare perrache', 'Gare perrache'),
            ('Hôtel ibis lyon 7', 'Hôtel ibis lyon 7'),
            ('place Bellecour', 'place Bellecour'),
            ('Autre', 'Autre'),
            ]
    lieu_depart = models.CharField(
        max_length=100,
        choices=lieu_prise_en_charge_choix,
        default='Aéroport saint exupery'
    )
    lieu_retour = models.CharField(
        max_length=100,
        choices=lieu_du_retour_choix,
        default='Aéroport saint exupery'
    )
   
    code_location = models.CharField(max_length=12, unique=True, editable=False, blank=True, null=True)
    status_choix= [
        ('accepté', 'accepté'),
        ('rejeté', 'rejeté'),
        ('encours', 'encours'),
    ]
    status = models.CharField(
        max_length=20,
        choices=status_choix,
        default='encours'
    )
    mysignature = models.CharField(
        max_length=20,
         default='not yet'
    )
    deal = models.CharField(
        max_length=20,
        default='disponible'
    )
     
    yousign_request_id = models.CharField(
    max_length=100,
    blank=True,
    null=True
    )
    
    yousign_document_id = models.CharField(
    max_length=255,
    null=True,
    blank=True
    )
          
    signed_contract_pdf = models.FileField(
        upload_to=signed_location_contrat_path,
        null=True,
        blank=True
    )
    
    #generate the pdf after approuve:
    contrat_pdf = models.FileField(
        upload_to=pdf_location_contrat_path,
        blank=True,
        null=True
    )
    
    facture_pdf = models.FileField(
        upload_to=facture_path,
        blank=True,
        null=True
    )
    
    def __str__(self):
        return f"Dossier #{self.id} - {self.nom_complet}"
    
    # Generate a unique code for the dossier location before saving
    def save(self, *args, **kwargs):
        if not self.code_location:
            characters = string.ascii_uppercase + string.digits
            while True:
                code = ''.join(secrets.choice(characters) for _ in range(12))
                if not DossierLocation.objects.filter(code_location=code).exists():
                    self.code_location = code
                    break

        super().save(*args, **kwargs)
        


class payementLocation(models.Model):
 
    location = models.ForeignKey(
        DossierLocation,
        on_delete=models.CASCADE,
        related_name="location_cars"
    )

    stripe_session_id = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    stripe_payment_intent = models.CharField(
            max_length=255,
            null=True,
            blank=True
        )
    
    stripe_customer_id = models.CharField(
            max_length=255,
            null=True,
            blank=True
        )
    
    paid_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    
    paid_currency = models.CharField(
            max_length=10,
            null=True,
            blank=True
        )

    paid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)