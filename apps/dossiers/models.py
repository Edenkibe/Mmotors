import secrets
import string

from django.db import models
import uuid
from django.db import models
from apps.accounts.models import User
from apps.voiture.models import Voiture
from datetime import timedelta 
from django.utils import timezone


#on cree le dossier ou sera stocker les fichiers:

#url du piece d identité
def file_place_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f'{instance.vehicule.type}/{instance.client.username}-{instance.vehicule.marque}/{filename}'

#url du generated pdf
def pdf_contrat_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f' contrat/{instance.client.first_name}/{instance.client.last_name}-{instance.vehicule.marque}/{filename}'

#url du signed contrat pdf pdf
def signed_contrat_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f' signed/{instance.client.first_name}/{instance.client.last_name}-{instance.vehicule.marque}/{filename}'

#url du signed contrat pdf pdf
def facture_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f' invoice/{instance.client.first_name}/{instance.client.last_name}-{instance.vehicule.marque}/{filename}'

class DossierAchat(models.Model):
 
    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="dossiers_achat_users"
    )

    vehicule = models.ForeignKey(
        Voiture,
        on_delete=models.CASCADE,
        related_name="dossiers_voitures"
    )

    # Informations personnelles
    nom_complet = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)
    email = models.EmailField()
    adresse = models.TextField()

    # Documents
    piece_identite = models.FileField(upload_to=file_place_path)
    
    # code unique du dossier pour l identification du dossier et le suivi de l etat du dossier:
    code_dossier = models.CharField(
        max_length=10,
        unique=True,
        editable=False,
        blank=True,
        null=True
    )
    read = models.CharField(
            max_length=10,
            default='non lu'
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    verification_choise= [
        ('pending...', 'pending...'),
        ('accepté', 'accepté'),
        ('rejeté', 'rejeté'),
    ]
    verification = models.CharField(
        max_length=20,
        choices=verification_choise,
        default='pending...'
    )
    message = models.TextField( blank=True,null=True)
    mysignature = models.CharField(max_length=20,default='not yet')
   
   #generate the pdf after approuve
    contrat_pdf = models.FileField(
        upload_to=pdf_contrat_path,
        blank=True,
        null=True
    )
    
    facture_pdf = models.FileField(
        upload_to=facture_path,
        blank=True,
        null=True
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
        upload_to=signed_contrat_path,
        null=True,
        blank=True
    )
    
    deal = models.CharField(
            max_length=20,
            default='encours'
        )
    
    # Stripe information
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

    paid_at = models.DateTimeField(
        null=True,
        blank=True
    )
    
    def __str__(self):
        return f"Dossier #{self.id} - {self.nom_complet}"
    
    # Generate a unique code for the dossier before saving
    def save(self, *args, **kwargs):
        if not self.code_dossier:
            characters = string.ascii_uppercase + string.digits
            while True:
                code = ''.join(secrets.choice(characters) for _ in range(10))
                if not DossierAchat.objects.filter(code_dossier=code).exists():
                    self.code_dossier = code
                    break

        super().save(*args, **kwargs)
        
    #to get the time ago of paid_at
    
    @property
    def since_created(self):
            """
            Retourne 'il y a X' pour le temps écoulé depuis paid_at
            """
            now = timezone.now()
            diff = now - self.paid_at
    
            if diff < timedelta(minutes=1):
                return "à l'instant"
            elif diff < timedelta(hours=1):
                minutes = int(diff.total_seconds() / 60)
                return f"il y a {minutes} minute{'s' if minutes > 1 else ''}"
            elif diff < timedelta(days=1):
                hours = int(diff.total_seconds() / 3600)
                return f"il y a {hours} heure{'s' if hours > 1 else ''}"
            elif diff < timedelta(days=30):
                days = diff.days
                return f"il y a {days} jour{'s' if days > 1 else ''}"
            elif diff < timedelta(days=365):
                months = int(diff.days / 30)
                return f"il y a {months} mois"
            else:
                years = int(diff.days / 365)
                return f"il y a {years} an{'s' if years > 1 else ''}"    