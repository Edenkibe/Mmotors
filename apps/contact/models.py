from django.db import models

# Create your models here.
from django.db import models

class ContactDossier(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    code_dossier = models.CharField(max_length=12)
    type_choix= [
        ('Achat', 'Achat'),
        ('Location', 'Location'),
    ]
    type= models.CharField(
         max_length=20,
        choices=type_choix,
         default='none'
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code_dossier} - {self.nom}"