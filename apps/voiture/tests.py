
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

from django.db.models import Count, Exists, OuterRef

from apps.voiture.models import Voiture


class VenteCarTest(TestCase):

    def setUp(self):
        # Créer un utilisateur
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        self.client = Client()

        # Connexion forcée de l'utilisateur avec force_login pour simuler un utilisateur connecté
        self.client.force_login(self.user)

        # Créer une voiture disponible pour l'achat
        self.car1 = Voiture.objects.create(
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

        # Créer une voiture non visible pour achat
        self.car2 = Voiture.objects.create(
            marque="BMW",
            type="Achat",
            disponibilite="Invisible",
            modele="X5",
            annee=2019,
            prix=30000,
            carburant="Diesel",
            boite="Manuelle",
            kilometre=75000,
            etat="Bon",
            description="Voiture en excellent état"
        )


    def test_vente_car(self):
        # Vérifier que la page fonctionne correctement

        response = self.client.get(reverse("voitures:vente_car"))

        self.assertEqual(response.status_code, 200)

    def test_vente_car_uses_correct_template(self):
        #Vérifier que le bon template est utilisé.

        response = self.client.get(reverse("voitures:vente_car"))

        self.assertTemplateUsed(response, "car_vente.html")

    def test_vente_car_displays_only_visible_cars_for_achat(self):
        """Vérifier que seules les voitures visibles pour achat sont récupérées."""

        response = self.client.get(reverse("voitures:vente_car"))

        cars = response.context["cars"]

        self.assertEqual(cars.count(), 1)
        self.assertIn(self.car1, cars)
        self.assertNotIn(self.car2, cars)


