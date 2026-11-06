
from django.test import TestCase
from django.test import TestCase, Client
from django.template.response import TemplateResponse
from django.urls import reverse
from django.contrib.auth import get_user_model
User = get_user_model()
from apps.dossiers.models import DossierAchat
from django.contrib.auth import get_user_model
from apps.voiture.models import Voiture
from django.contrib.messages import get_messages
from apps.voiture.forms.voitureForm import typeForm
from apps.dossiers.form.reply_demandeForm import ReplydossierForm
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch, MagicMock


User = get_user_model()

# test sur la recherche des voitures vendues dans la page d'administration
class SearchActionTest(TestCase):

    def setUp(self):
            self.client = Client()
           # Créer un utilisateur
            self.user = User.objects.create_user(
                username='testuser',
                email='test@example.com',
                password='testpass123',
                first_name="Jean",
                last_name="Dupont"
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
    
            self.dossier1 = DossierAchat.objects.create(
                code_dossier="DOSSIER001",
                nom_complet="Pierre Martin",
                telephone="06 11 22 33 44",
                adresse="789 Boulevard Saint-Germain",
                email="pierre.martin@example.com",
                piece_identite="Passeport",
                client=self.user,
                vehicule=self.car1,
                deal="acheté",
                read="non lu"
            )
    
            self.dossier2 = DossierAchat.objects.create(
                code_dossier="DOSSIER002",
                nom_complet="Jean Dupont",
                telephone="06 12 34 56 78",
                adresse="123 Rue de la Paix",
                email="jean.dupont@example.com",
                piece_identite="Passeport",
                client=self.user,
                vehicule=self.car1,
                deal="acheté",
                read="non lu"
            )
    
            self.dossier3 = DossierAchat.objects.create(
                code_dossier="ABC123",
                nom_complet="Marie Curie",
                telephone="06 98 76 54 32",
                adresse="456 Avenue des Champs-Élysées",
                email="marie.curie@example.com",
                piece_identite="Carte d'identité",
                client=self.user,
                vehicule=self.car1,
                deal="disponible",
                read="lu"
            )
    
            self.url = reverse("dossiers:search_dossier")

    def test_search_empty_query(self):
        """Une recherche vide retourne tous les dossiers achetés."""

        response = self.client.get(
            reverse("core:search_action"),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["action"]), 2)
        self.assertEqual(response.context["total"], 2)

    def test_search_by_code_dossier(self):
        """Recherche par code de dossier."""

        response = self.client.get(
            reverse("core:search_action"),
            {"q": "DOSSIER001"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total"], 1)
        self.assertEqual(
            response.context["action"].first().code_dossier,
            "DOSSIER001"
        )

    def test_search_by_first_name(self):
        """Recherche par prénom du client."""

        response = self.client.get(
            reverse("core:search_action"),
            {"q": "test"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )

        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(response.context["total"], 0)

    def test_search_one_character(self):
        """Un seul caractère ne doit retourner aucun résultat."""

        response = self.client.get(
            reverse("core:search_action"),
            {"q": "D"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total"], 0)

    def test_search_no_result(self):
        """Une recherche inexistante retourne zéro résultat."""

        response = self.client.get(
            reverse("core:search_action"),
            {"q": "INEXISTANT"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total"], 0)

    def test_ajax_template(self):
        """Vérifie que le bon template AJAX est utilisé."""

        response = response = self.client.get(
            reverse("core:search_action"),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )

        self.assertTemplateUsed(response, "ajax/action_ajax.html")
        

#test la fonction de basculer la voiture de type achat vers location et vice versa
class BasculerTypeTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )

        self.client.force_login(self.user)

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

        self.car2 = Voiture.objects.create(
            marque="BMW",
            type="Location",
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

        self.url = reverse(
            "core:basculer_type",
            kwargs={"id": self.car1.id}
        )

    def test_get_basculer_type(self):
        """Vérifie l'affichage de la page."""

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(
            response,
            "admin_template/bascule_type.html"
        )

        self.assertEqual(
            response.context["get_car"],
            self.car1
        )

        self.assertIsInstance(
            response.context["form"],
            typeForm
        )

    def test_achat_vers_location(self):
        """Vérifie le passage de Achat vers Location."""

        response = self.client.post(
            self.url,
            {
                "prix": 20000,
                "type": "Location"
            }
        )

        self.car1.refresh_from_db()

        self.assertEqual(self.car1.type, "Location")
        self.assertRedirects(response, self.url)

    def test_location_vers_achat(self):
        """Vérifie le passage de Location vers Achat."""

        self.car1.type = "Location"
        self.car1.save()

        response = self.client.post(
            self.url,
            {
                "prix": 20000,
                "type": "Achat"
            }
        )

        self.car1.refresh_from_db()

        self.assertEqual(self.car1.type, "Achat")
        self.assertRedirects(response, self.url)

    def test_message_success(self):
        response = self.client.post(
            self.url,
            {
                "prix": 20000,
                "type": "Achat",  # Must match a valid model choice
            },
            follow=True
        )

        self.assertEqual(response.status_code, 200)

        messages_list = [
            str(message)
            for message in get_messages(response.wsgi_request)
        ]

        self.assertIn(
            "car has been edited successfully",
            messages_list
        )

    def test_voiture_not_found(self):
        """Vérifie qu'une voiture inexistante retourne 404."""

        url = reverse(
            "core:basculer_type",
            kwargs={"id": 999999}
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_invalid_form(self):

        ancien_type = self.car1.type

        response = self.client.post(
            self.url,
            {
                "prix": 20000,
                "type": "valeur_invalide"
            }
        )

        self.car1.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.car1.type, ancien_type)

        

#test pour la function de repondre a une demande achat d'un client dans la page d'administration:
class RepondreTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123"
        )
        self.client.force_login(self.user)

        self.car = Voiture.objects.create(
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

        self.dossier = DossierAchat.objects.create(
            code_dossier="DOSSIER001",
            nom_complet="Jean Dupont",
            client=self.user,
            vehicule=self.car,
            deal="acheté",
            read="non lu",
            email=self.user.email,
            verification="pending...",
        )

        self.url = reverse(
            "core:repondre",
            kwargs={"id": self.dossier.id}
        )

    def get_messages_list(self, response):
        return [
            str(message)
            for message in get_messages(response.wsgi_request)
        ]

    # 1. Vérifier que la page s'affiche correctement
    def test_get_repondre(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "administration/repondre_demande.html"
        )

        self.assertEqual(
            response.context["demandes"],
            self.dossier
        )

        self.assertIsInstance(
            response.context["form"],
            ReplydossierForm
        )

    # 2. Vérifier qu'un dossier inexistant retourne 404
    def test_dossier_not_found(self):
        url = reverse(
            "core:repondre",
            kwargs={"id": 999999}
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    # 3. Vérifier une réponse sans acceptation
    def test_repondre_demande_refusee(self):
        response = self.client.post(
            self.url,
            {"verification": "rejeté"},
            follow=True
        )

        print("Status:", response.status_code)
        print("URL:", response.redirect_chain)

        if response.context:
            print("Form errors:", response.context["form"].errors)

        self.dossier.refresh_from_db()

        print("Statut après POST:", self.dossier.verification)

        self.assertEqual(
            self.dossier.verification,
            "rejeté"
        )

    # 4. Vérifier qu'une demande déjà acceptée est simplement mise à jour
    @patch("apps.core.yousignservice.YousignClient")
    def test_demande_deja_acceptee(self, mock_yousign):
        self.dossier.verification = "accepté"
        self.dossier.save()

        response = self.client.post(
            self.url,
            {"verification": "accepté"},
            follow=True
        )

        self.assertEqual(response.status_code, 200)

        messages_list = self.get_messages_list(response)

        self.assertIn(
            "La demande a été mise à jour.",
            messages_list
        )

        # Yousign ne doit pas être appelé une deuxième fois
        mock_yousign.assert_not_called()

    # 5. Vérifier qu'un formulaire invalide ne redirige pas
    def test_formulaire_invalide(self):
        response = self.client.post(
            self.url,
            {"verification": "valeur_invalide"}
        )

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(
            response,
            "administration/repondre_demande.html"
        )

        self.assertTrue(response.context["form"].errors)

    # 6. Vérifier l'échec de Yousign
    @patch("apps.core.yousignservice.YousignClient")
    def test_erreur_yousign(self, mock_yousign):
        mock_yousign.return_value.generate_contract.side_effect = (
            Exception("Erreur Yousign")
        )

        response = self.client.post(
            self.url,
            {"verification": "accepté"},
            follow=True
        )

        self.assertEqual(response.status_code, 200)

        messages_list = self.get_messages_list(response)

        self.assertIn(
            "Erreur lors de la création du contrat Yousign",
            messages_list
        )
