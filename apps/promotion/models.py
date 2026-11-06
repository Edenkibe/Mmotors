from datetime import timedelta
import re
from django.utils import timezone
from django.db import models
from django.conf import settings
from django.forms import ValidationError
from apps.voiture.models import Voiture

# Create your models here

class Promotion(models.Model):  
    creator=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True,related_name="user_promotion")
    voiture= models.ForeignKey(
        Voiture,
        on_delete=models.CASCADE,
        related_name="voiture_promotion",
    )
    titre = models.CharField(max_length=100)
    description = models.TextField()
    disponibilite_choise= [
        ('disponible', 'disponible'),
        ('commencé', 'commencé'),
        ('promotion done', 'promotion done'),
        ('Bloqué', 'Bloqué'),
    ]
    disponibilite=models.CharField(
        max_length=20,
        choices=disponibilite_choise,
        default='disponible'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    promotion_done_at = models.DateTimeField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    
     #to get the time ago of created_at 
    @property
    def time_since_created(self):
        """
        Retourne 'il y a X' pour le temps écoulé depuis created_at
        """
        now = timezone.now()
        diff = now - self.created_at

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
   
  #to get the time ago of accepted_at 
    @property
    def time_since_started(self):
        """
        Retourne 'il y a X' pour le temps écoulé depuis accepted_at
        """
        now = timezone.now()
        diff = now - self.start_date

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
   
   
    #to get the time ago of done promotion 
    @property
    def time_since_end(self):
        """
        Retourne 'il y a X' pour le temps écoulé depuis accepted_at
        """
        now = timezone.now()
        diff = now - self.promotion_done_at

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
   
   