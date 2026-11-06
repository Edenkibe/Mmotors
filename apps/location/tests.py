
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()
from unittest.mock import patch

from apps.location.models import DossierLocation
from apps.voiture.models import Voiture

class CreerDossierLocationTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.client = Client()
        
        # Connexion forcée de l'utilisateur avec force_login pour simuler un utilisateur connecté
        self.client.force_login(self.user)

        self.voiture = Voiture.objects.create(
        # Créer une voiture disponible pour l'achat                 
            marque="Toyota",
            type="Achat",
            disponibilite="Visible",          
            modele="Corolla",
            annee=2020,
            prix=20000,
            carburant="Essence",
            boite="Automatique",
            kilometre=50000,
            etat="Bon",
            description="Voiture en parfait état"
                   
        )

        self.url = reverse(
            "locations:creer_dossier_location",
            kwargs={"id": self.voiture.id}
        )

    def test_affichage_page_get(self):
        """Vérifie que la page s'affiche correctement avec GET."""

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "depot_location.html")

        self.assertIn("form", response.context)
        self.assertEqual(response.context["voiture"], self.voiture)
        self.assertFalse(response.context["dossier_exist"])
        self.assertEqual(response.context["count"], 0)

    def test_creation_dossier_post_valide(self):
        """Vérifie la création d'un dossier avec un formulaire valide."""

        data = {
             "nom_complet": "Jean Dupont",
            "telephone": "0612345678",
            "email": "jean.dupont@example.com",
            "adresse": "10 rue de Paris",
            "numero_permis": "PERMIS123456",
            "pays_delivrance_permis": "France",
            "date_depart": "2026-12-01",
            "date_retour": "2026-12-05",
            "lieu_depart": "Aéroport saint exupery",
            "lieu_retour": "Aéroport saint exupery",
        }

        response = self.client.post(self.url, data)

        # Vérifier que le formulaire est valide
        if response.status_code == 200:
            print("Erreurs du formulaire :", response.context["form"].errors)

        # Vérifier la création du dossier
        self.assertEqual(DossierLocation.objects.count(), 1)

        dossier = DossierLocation.objects.first()

        # Vérifier les associations
        self.assertEqual(dossier.client, self.user)
        self.assertEqual(dossier.vehicule, self.voiture)

        # Vérifier la redirection
        self.assertRedirects(
            response,
            reverse(
                "locations:user_satisfaction_location",
                kwargs={"id": dossier.id}
            )
        )


    def test_post_formulaire_invalide(self):
        """Vérifie qu'un formulaire invalide ne crée aucun dossier."""

        response = self.client.post(self.url, {})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(DossierLocation.objects.count(), 0)
        self.assertTemplateUsed(response, "depot_location.html")

        self.assertFalse(response.context["form"].is_valid())

    def test_dossier_exist_true(self):
        """Vérifie que dossier_exist retourne True si un dossier correspondant existe."""

        DossierLocation.objects.create(
            client=self.user,
            vehicule=self.voiture,
            status="accepté",
            mysignature="not yet",
            deal=["disponible"],
            nom_complet="Nom et prénom",
            telephone="Téléphone",
            email="Email",
            adresse="Adresse complète",
            numero_permis="Numéro du permis de conduire",
            pays_delivrance_permis="Pays",
            date_depart="2023-01-01 10:00:00",
            date_retour="2023-01-01 18:00:00",
            lieu_depart="Lieu de prise en charge",
            lieu_retour="Lieu de restitution",
            # Ajoute les autres champs obligatoires
        )

        response = self.client.get(self.url)

        self.assertTrue(response.context["dossier_exist"])

    def test_dossier_exist_false(self):
        """Vérifie que dossier_exist retourne False sans dossier correspondant."""

        response = self.client.get(self.url)

        self.assertFalse(response.context["dossier_exist"])

    def test_count_dossiers(self):
        """Vérifie que count compte uniquement les dossiers encours et acceptés."""

        DossierLocation.objects.create(
            client=self.user,
            vehicule=self.voiture,
            status="encours",
            nom_complet="Nom et prénom",
            telephone="Téléphone",
            email="Email",
            adresse="Adresse complète",
            numero_permis="Numéro du permis de conduire",
            pays_delivrance_permis="Pays",
            date_depart="2023-01-01 10:00:00",
            date_retour="2023-01-01 18:00:00",
            lieu_depart="Lieu de prise en charge",
            lieu_retour="Lieu de restitution",
            # Ajoute les autres champs obligatoires
        )

        DossierLocation.objects.create(
            client=self.user,
            vehicule=self.voiture,
            status="accepté",
            nom_complet="Nom et prénom",
            telephone="Téléphone",
            email="Email",
            adresse="Adresse complète",
            numero_permis="Numéro du permis de conduire",
            pays_delivrance_permis="france",
            date_depart="2023-01-01 10:00:00",
            date_retour="2023-01-01 18:00:00",
            lieu_depart="Lieu de prise en charge",
            lieu_retour="Lieu de restitution",
            # Ajoute les autres champs obligatoires
        )

        response = self.client.get(self.url)

        self.assertEqual(response.context["count"], 2)

    def test_voiture_inexistante(self):
        """Vérifie qu'une erreur 404 est retournée si la voiture n'existe pas."""

        response = self.client.get(
            reverse(
                "locations:creer_dossier_location",
                kwargs={"id": 999999}
            )
        )

        self.assertEqual(response.status_code, 404)
        
        

