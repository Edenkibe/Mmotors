from django.db import models
from datetime import timedelta
from django.utils import timezone

# Create your models here.
class Voiture(models.Model):
    marque = models.CharField(max_length=100)
    modele = models.CharField(max_length=100)
    annee = models.IntegerField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    carburant_choise= [
        ('Diesel', 'Diesel'),
        ('hybride', 'hybride'),
        ('electrique', 'electrique'),
        ('essence', 'essence'),
    ]
    boite_choise= [
        ('Manuel', 'Manuel'),
        ('automatique', 'automatique'),
    ]
    disponibilite_choise= [
        ('visible', 'visible'),
        ('invisible', 'invisible'),
    ]
    disponibilite=models.CharField(
        max_length=20,
        choices=disponibilite_choise,
        default='visible'
    )
    boite=models.CharField(
        max_length=20,
        choices=boite_choise,
        default='available'
    )
    carburant=models.CharField(
        max_length=20,
        choices=carburant_choise,
        default='available'
    )
    kilometre = models.PositiveIntegerField(
        default=0,
        help_text="Kilométrage du véhicule en km"
    )
    Status_choices = [
        ('Occasion', 'Occasion'),
        ('New', 'New'),
        ('super', 'super'),
    ]
    etat = models.CharField(
        max_length=20,
        choices=Status_choices,
        default='available'
    )
    type_CHOICES = [
        ('Location', 'Location'),
        ('Achat', 'Achat'),
    ]
    type = models.CharField(max_length=100, choices=type_CHOICES, default='Achat')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.marque + " " + self.modele
    
    #pour ciblé la photo principale sur l annonce
    def main_photo(self):
        return self.photos.filter(is_main=True).first()

    #to get the time ago of voiture added 
    @property
    def since_created(self):
        """
        Retourne 'il y a X' pour le temps écoulé depuis created_at
        """
        now = timezone.now()
        diff = now - self.date_added

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
        

class Photo(models.Model):
    voiture = models.ForeignKey(
        Voiture,
        on_delete=models.CASCADE,
        related_name="photos" 
    )
    image = models.ImageField(upload_to="voitures/")
    date_added = models.DateTimeField(auto_now_add=True)
    is_main = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Photo {self.voiture.modele}"
    
    
    #getting the voiture image url to display it in the template
    @property
    def get_picture_url(self):
        if self.image:
            return self.image.url
        return ""