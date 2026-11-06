from urllib import response

from django.utils import timezone
from datetime import datetime

from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from apps.location.models import DossierLocation
from django.contrib.auth import get_user_model
User = get_user_model()
from apps.contact.models import ContactDossier
from apps.voiture.models import Voiture

# affichage du formulaire de contact et test du formulaire
class ContactDossierTestCase(TestCase):

    def setUp(self):
        self.client_obj = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.vehicule = Voiture.objects.create(
            marque='Peugeot',
            modele='308 GT',
            annee=2020,
            prix=15000.00,
            type='Achat',
            carburant='essence',
            boite='Manuel',
            kilometre=50000,
            etat='Occasion',
            description='Une voiture en bon état.',
        )
        
        self.contact_url = reverse('contact:contact_dossier')
        self.dossier = DossierLocation.objects.create(
            code_location='S5L4Y2YMF130',
            client=self.client_obj,
            vehicule=self.vehicule,
            date_depart = timezone.make_aware(datetime(2026, 11, 1, 10, 0)),
            date_retour=timezone.make_aware(datetime(2026, 11, 1, 10, 0))
            # Ajouter les autres champs obligatoires
        )

    # test affichage du formulaire de contact:
    def test_contact_page_get(self):
        response = self.client.get(self.contact_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertIn('form', response.context)
        
    # test envoie du formulaire de contact avec un patch pour simuler l'envoi d'email   
    @patch('apps.contact.views.send_contact_email')
    def test_contact_success(self, mock_send_email):
        data = {
            'nom': 'Jean Dupont',
            'email': 'jean@example.com',
            'code_dossier': self.dossier.code_location,
            'type': 'Location',
            'message': 'Bonjour, je souhaite obtenir des informations.'
        }

        response = self.client.post(self.contact_url, data)

        print("STATUS:", response.status_code)
        print("URL:", getattr(response, 'url', None))

        self.assertEqual(response.status_code, 302)
        
    # test invalide du formulaire:  
    @patch('apps.contact.views.send_contact_email')
    def test_contact_invalid_form(self, mock_send_email):
        response = self.client.post(self.contact_url, {})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

        mock_send_email.assert_not_called()    