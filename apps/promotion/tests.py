
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

from apps.promotion.forms.promoForm import promotionForm
from apps.promotion.forms.promoForm import promotionForm
from apps.promotion.models import Promotion
from apps.voiture.models import Photo, Voiture

User = get_user_model()


class CreatePromotionTest(TestCase):

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
        
        self.url = reverse(
        "promotion:create_promotion",
        kwargs={"id": self.car1.id}
        )


    def test_create_promotion_get(self):
        """Vérifier l'affichage du formulaire."""

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "create_pub.html")

        self.assertIsInstance(
            response.context["form"],
            promotionForm
        )

        self.assertEqual(
            response.context["get_car"],
            self.car1
        )

    def test_create_promotion_displays_photos(self):
        """Vérifier que les photos de la voiture sont récupérées."""

        response = self.client.get(self.url)

        self.assertQuerySetEqual(
            response.context["photos"],
            Photo.objects.filter(voiture=self.car1),
            ordered=False
        )

    def test_create_promotion_post_valid(self):
        """Vérifier la création d'une promotion."""

        data = {
            "titre": "Toyota Camry",
            "description": "Promotion exceptionnelle",
            "start_date": "2023-12-01",
            "end_date": "2023-12-31",
            "voiture": self.car1,
            "creator": self.user,
            "disponibilite": "disponible"
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            Promotion.objects.count(),
            1
        )

        promotion = Promotion.objects.first()

        self.assertEqual(promotion.voiture, self.car1)
        self.assertEqual(promotion.creator, self.user)
        self.assertEqual(promotion.disponibilite, "disponible")

    def test_create_promotion_post_invalid(self):
        """Vérifier que le formulaire invalide ne crée rien."""

        response = self.client.post(self.url, {})

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "create_pub.html")

        self.assertEqual(
            Promotion.objects.count(),
            0
        )

        self.assertFalse(response.context["form"].is_valid())

    def test_create_promotion_redirects_to_car_details(self):
        """Vérifier la redirection après création."""

        data = {
            "titre": "Toyota Camry",
            "description": "Voiture de luxe",
            "start_date": "2023-01-01",
            "end_date": "2023-12-31"
        }

        response = self.client.post(self.url, data)

        if response.status_code == 302:
            self.assertRedirects(
                response,
                reverse(
                    "core:car_details",
                    kwargs={"id": self.car1.id}
                ),
                fetch_redirect_response=False
            )

    def test_create_promotion_car_not_found(self):
        """Vérifier le comportement si la voiture n'existe pas."""

        url = reverse(
            "promotion:create_promotion",
            kwargs={"id": 999999}
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
