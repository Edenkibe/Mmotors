from unittest.mock import MagicMock, patch

import requests
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import Client, SimpleTestCase, TestCase, override_settings
from django.urls import reverse

from apps.core.yousignservice import YousignClient
from apps.dossiers.form.reply_demandeForm import ReplydossierForm
from apps.dossiers.models import DossierAchat
from apps.voiture.forms.voitureForm import typeForm
from apps.voiture.models import Voiture

User = get_user_model()


# test sur la recherche des voitures vendues dans la page d'administration
class SearchActionTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Créer un utilisateur
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            first_name="Jean",
            last_name="Dupont",
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
            description="Voiture en parfait état",
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
            description="Voiture en excellent état",
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
            read="non lu",
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
            read="non lu",
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
            read="lu",
        )

        self.url = reverse("dossiers:search_dossier")

    def test_search_empty_query(self):
        """Une recherche vide retourne tous les dossiers achetés."""

        response = self.client.get(
            reverse("core:search_action"), HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["action"]), 2)
        self.assertEqual(response.context["total"], 2)

    def test_search_by_code_dossier(self):
        """Recherche par code de dossier."""

        response = self.client.get(
            reverse("core:search_action"),
            {"q": "DOSSIER001"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total"], 1)
        self.assertEqual(response.context["action"].first().code_dossier, "DOSSIER001")

    def test_search_by_first_name(self):
        """Recherche par prénom du client."""

        response = self.client.get(
            reverse("core:search_action"),
            {"q": "test"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(response.context["total"], 0)

    def test_search_one_character(self):
        """Un seul caractère ne doit retourner aucun résultat."""

        response = self.client.get(
            reverse("core:search_action"),
            {"q": "D"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total"], 0)

    def test_search_no_result(self):
        """Une recherche inexistante retourne zéro résultat."""

        response = self.client.get(
            reverse("core:search_action"),
            {"q": "INEXISTANT"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total"], 0)

    def test_ajax_template(self):
        """Vérifie que le bon template AJAX est utilisé."""

        response = response = self.client.get(
            reverse("core:search_action"), HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )

        self.assertTemplateUsed(response, "ajax/action_ajax.html")


# test la fonction de basculer la voiture de type achat vers location et vice versa
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
            description="Voiture en parfait état",
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
            description="Voiture en excellent état",
        )

        self.url = reverse("core:basculer_type", kwargs={"id": self.car1.id})

    def test_get_basculer_type(self):
        """Vérifie l'affichage de la page."""

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "admin_template/bascule_type.html")

        self.assertEqual(response.context["get_car"], self.car1)

        self.assertIsInstance(response.context["form"], typeForm)

    def test_achat_vers_location(self):
        """Vérifie le passage de Achat vers Location."""

        response = self.client.post(self.url, {"prix": 20000, "type": "Location"})

        self.car1.refresh_from_db()

        self.assertEqual(self.car1.type, "Location")
        self.assertRedirects(response, self.url)

    def test_location_vers_achat(self):
        """Vérifie le passage de Location vers Achat."""

        self.car1.type = "Location"
        self.car1.save()

        response = self.client.post(self.url, {"prix": 20000, "type": "Achat"})

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
            follow=True,
        )

        self.assertEqual(response.status_code, 200)

        messages_list = [
            str(message) for message in get_messages(response.wsgi_request)
        ]

        self.assertIn("car has been edited successfully", messages_list)

    def test_voiture_not_found(self):
        """Vérifie qu'une voiture inexistante retourne 404."""

        url = reverse("core:basculer_type", kwargs={"id": 999999})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_invalid_form(self):

        ancien_type = self.car1.type

        response = self.client.post(
            self.url, {"prix": 20000, "type": "valeur_invalide"}
        )

        self.car1.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.car1.type, ancien_type)


# test pour la function de repondre a une demande achat d'un client dans la page d'administration:
class RepondreTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password123"
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
            description="Voiture en parfait état",
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

        self.url = reverse("core:repondre", kwargs={"id": self.dossier.id})

    def get_messages_list(self, response):
        return [str(message) for message in get_messages(response.wsgi_request)]

    # 1. Vérifier que la page s'affiche correctement
    def test_get_repondre(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "administration/repondre_demande.html")

        self.assertEqual(response.context["demandes"], self.dossier)

        self.assertIsInstance(response.context["form"], ReplydossierForm)

    # 2. Vérifier qu'un dossier inexistant retourne 404
    def test_dossier_not_found(self):
        url = reverse("core:repondre", kwargs={"id": 999999})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    # 3. Vérifier une réponse sans acceptation
    def test_repondre_demande_refusee(self):
        response = self.client.post(self.url, {"verification": "rejeté"}, follow=True)

        print("Status:", response.status_code)
        print("URL:", response.redirect_chain)

        if response.context:
            form = response.context.get("form")

            if form:
                print("Form errors:", form.errors)
            else:
                print("Aucun formulaire dans le contexte.")

        self.dossier.refresh_from_db()

        print("Statut après POST:", self.dossier.verification)

        self.assertEqual(self.dossier.verification, "rejeté")

    # 4. Vérifier qu'une demande déjà acceptée est simplement mise à jour
    @patch("apps.core.yousignservice.requests.request")
    def test_demande_deja_acceptee(self, mock_yousign):
        self.dossier.verification = "accepté"
        self.dossier.save()

        response = self.client.post(self.url, {"verification": "accepté"}, follow=True)

        self.assertEqual(response.status_code, 200)

        messages_list = self.get_messages_list(response)

        self.assertIn("La demande a été mise à jour.", messages_list)

        # Yousign ne doit pas être appelé une deuxième fois
        mock_yousign.assert_not_called()

    # 5. Vérifier qu'un formulaire invalide ne redirige pas
    def test_formulaire_invalide(self):
        response = self.client.post(self.url, {"verification": "valeur_invalide"})

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "administration/repondre_demande.html")

        self.assertTrue(response.context["form"].errors)

    # 6. Vérifier l'échec de Yousign
    @patch("apps.core.yousignservice.requests.request")
    def test_erreur_yousign(self, mock_yousign):
        mock_yousign.return_value.generate_contract.side_effect = Exception(
            "Erreur Yousign"
        )

        response = self.client.post(self.url, {"verification": "accepté"}, follow=True)

        self.assertEqual(response.status_code, 200)

        messages_list = self.get_messages_list(response)

        self.assertIn("Erreur lors de la création du contrat Yousign", messages_list)

@override_settings(
    YOUSIGN_BASE_URL="https://api-sandbox.yousign.app/v3",
    YOUSIGN_API_KEY="fake-api-key",
)
class TestYousignClient(SimpleTestCase):

    def setUp(self):
        self.client = YousignClient()

    # -------------------------------------------------
    # 1. TEST INITIALISATION
    # -------------------------------------------------

    def test_client_initialization(self):
        self.assertEqual(
            self.client.base_url,
            "https://api-sandbox.yousign.app/v3"
        )

        self.assertEqual(
            self.client.api_key,
            "fake-api-key"
        )

        self.assertEqual(
            self.client.headers["Authorization"],
            "Bearer fake-api-key"
        )

    # -------------------------------------------------
    # 2. TEST CONFIGURATION MANQUANTE
    # -------------------------------------------------

    @override_settings(YOUSIGN_API_KEY="")
    def test_request_without_api_key(self):
        client = YousignClient()

        with self.assertRaises(RuntimeError) as context:
            client._request("GET", "/test")

        self.assertIn(
            "YouSign is not configured",
            str(context.exception)
        )

    # -------------------------------------------------
    # 3. TEST REQUEST SUCCESS
    # -------------------------------------------------

    @patch("apps.core.yousignservice.requests.request")
    def test_request_success(self, mock_request):

        mock_response = MagicMock()
        mock_response.status_code = 200

        mock_request.return_value = mock_response

        result = self.client._request(
            "GET",
            "https://api-sandbox.yousign.app/v3/test"
        )

        self.assertEqual(result, mock_response)

        mock_request.assert_called_once_with(
            "GET",
            "https://api-sandbox.yousign.app/v3/test",
            timeout=30,
            headers={
                "Authorization": "Bearer fake-api-key",
                "Accept": "application/json",
            }
        )

    # -------------------------------------------------
    # 4. TEST EXTRACTION ERREUR JSON
    # -------------------------------------------------

    def test_extract_error_detail_json(self):

        response = MagicMock()

        response.json.return_value = {
            "detail": "Invalid signer parameters"
        }

        result = self.client._extract_error_detail(response)

        self.assertEqual(
            result,
            "Invalid signer parameters"
        )

    # -------------------------------------------------
    # 5. TEST EXTRACTION ERREUR TEXTE
    # -------------------------------------------------

    def test_extract_error_detail_text(self):

        response = MagicMock()

        response.json.side_effect = ValueError()

        response.text = "Server error"

        result = self.client._extract_error_detail(response)

        self.assertEqual(result, "Server error")

    # -------------------------------------------------
    # 6. TEST ERREUR API 400
    # -------------------------------------------------

    @patch("apps.core.yousignservice.requests.request")
    def test_request_http_400(self, mock_request):

        mock_response = MagicMock()

        mock_response.status_code = 400
        mock_response.reason = "Bad Request"

        mock_response.json.return_value = {
            "detail": "Invalid signer parameters"
        }

        mock_response.raise_for_status.side_effect = requests.HTTPError(
            "400 Bad Request"
        )

        mock_request.return_value = mock_response

        with self.assertRaises(RuntimeError) as context:

            self.client._request(
                "POST",
                "https://api-sandbox.yousign.app/v3/signers"
            )

        self.assertIn(
            "400 Bad Request",
            str(context.exception)
        )

        self.assertIn(
            "Invalid signer parameters",
            str(context.exception)
        )

        mock_response.raise_for_status.assert_called_once()

    # -------------------------------------------------
    # 7. TEST CREATION DEMANDE ACHAT
    # -------------------------------------------------

    @patch("apps.core.yousignservice.requests.request")
    def test_create_signature_request_achat(self, mock_request):

        demande = MagicMock()

        demande.id = 3
        demande.vehicule.marque = "Toyota"

        mock_response = MagicMock()

        mock_response.json.return_value = {
            "id": "request-123",
            "status": "draft"
        }

        mock_request.return_value = mock_response

        result = self.client.create_signature_request(
            demande,
            "achat"
        )

        self.assertEqual(result["id"], "request-123")

        args, kwargs = mock_request.call_args

        self.assertEqual(args[0], "post")

        self.assertEqual(
            kwargs["json"],
            {
                "name": "contrat voiture Toyota",
                "delivery_mode": "email",
                "external_id": "achat-3",
            }
        )

    # -------------------------------------------------
    # 8. TEST CREATION DEMANDE LOCATION
    # -------------------------------------------------

    @patch("apps.core.yousignservice.requests.request")
    def test_create_signature_request_location(self, mock_request):

        demande = MagicMock()

        demande.id = 5
        demande.vehicule.marque = "BMW"

        mock_response = MagicMock()

        mock_response.json.return_value = {
            "id": "request-456"
        }

        mock_request.return_value = mock_response

        result = self.client.create_signature_request(
            demande,
            "location"
        )

        self.assertEqual(result["id"], "request-456")

        payload = mock_request.call_args.kwargs["json"]

        self.assertEqual(
            payload["name"],
            "contrat location BMW"
        )

        self.assertEqual(
            payload["external_id"],
            "location-5"
        )

    # -------------------------------------------------
    # 9. TEST TYPE CONTRAT INVALIDE
    # -------------------------------------------------

    def test_invalid_contract_type(self):

        demande = MagicMock()

        with self.assertRaises(ValueError):
            self.client.create_signature_request(
                demande,
                "autre"
            )

    # -------------------------------------------------
    # 10. TEST AJOUT SIGNATAIRE SUCCESS
    # -------------------------------------------------

    @patch("apps.core.yousignservice.requests.request")
    def test_add_signer_success(self, mock_request):

        mock_response = MagicMock()

        mock_response.status_code = 201
        mock_response.text = '{"id": "signer-123"}'

        mock_response.json.return_value = {
            "id": "signer-123",
            "status": "initiated"
        }

        mock_request.return_value = mock_response

        result = self.client.add_signer(
            request_id="request-123",
            document_id="document-123",
            first_name="Jean",
            last_name="Dupont",
            email="jean@example.com"
        )

        self.assertEqual(result["id"], "signer-123")

        args, kwargs = mock_request.call_args

        self.assertEqual(args[0], "post")

        self.assertEqual(
            args[1],
            "https://api-sandbox.yousign.app/v3/signature_requests/request-123/signers"
        )

        payload = kwargs["json"]

        self.assertEqual(
            payload["info"]["first_name"],
            "Jean"
        )

        self.assertEqual(
            payload["info"]["last_name"],
            "Dupont"
        )

        self.assertEqual(
            payload["info"]["email"],
            "jean@example.com"
        )

        self.assertEqual(
            payload["signature_level"],
            "electronic_signature"
        )

        self.assertEqual(
            payload["fields"][0]["document_id"],
            "document-123"
        )

    # -------------------------------------------------
    # 11. TEST EMAIL INVALIDE
    # -------------------------------------------------

    def test_add_signer_invalid_email(self):

        with self.assertRaises(ValueError):

            self.client.add_signer(
                "request-123",
                "document-123",
                "Jean",
                "Dupont",
                ""
            )

        with self.assertRaises(ValueError):

            self.client.add_signer(
                "request-123",
                "document-123",
                "Jean",
                "Dupont",
                "email-invalide"
            )

    # -------------------------------------------------
    # 12. TEST ERREUR 400 LORS AJOUT SIGNATAIRE
    # -------------------------------------------------

    @patch("apps.core.yousignservice.requests.request")
    def test_add_signer_api_error_400(self, mock_request):

        mock_request.side_effect = RuntimeError(
            "YouSign API error: 400 Bad Request - Invalid signer parameters"
        )

        with self.assertRaises(RuntimeError) as context:

            self.client.add_signer(
                request_id="request-123",
                document_id="document-123",
                first_name="Jean",
                last_name="Dupont",
                email="jean@example.com"
            )

        self.assertIn(
            "400 Bad Request",
            str(context.exception)
        )

    # -------------------------------------------------
    # 13. TEST ACTIVATION SIGNATURE
    # -------------------------------------------------

    @patch("apps.core.yousignservice.requests.request")
    def test_activate_signature(self, mock_request):

        mock_response = MagicMock()

        mock_response.json.return_value = {
            "id": "request-123",
            "status": "ongoing"
        }

        mock_request.return_value = mock_response

        result = self.client.activate("request-123")

        self.assertEqual(result["status"], "ongoing")

        args, kwargs = mock_request.call_args

        self.assertEqual(args[0], "post")

        self.assertEqual(
            args[1],
            "https://api-sandbox.yousign.app/v3/signature_requests/request-123/activate"
        )

    # -------------------------------------------------
    # 14. TEST TELECHARGEMENT DOCUMENT SIGNE
    # -------------------------------------------------

    @patch("apps.core.yousignservice.requests.request")
    def test_download_signed_document(self, mock_request):

        mock_response = MagicMock()

        mock_response.content = b"FAKE PDF CONTENT"

        mock_request.return_value = mock_response

        result = self.client.download_signed_document(
            "request-123"
        )

        self.assertEqual(
            result,
            b"FAKE PDF CONTENT"
        )

        args, kwargs = mock_request.call_args

        self.assertEqual(args[0], "get")

        self.assertIn(
            "/documents/download",
            args[1]
        )

    # -------------------------------------------------
    # 15. TEST GENERATION CONTRAT TYPE INVALIDE
    # -------------------------------------------------

    def test_generate_contract_invalid_type(self):

        demande = MagicMock()

        with self.assertRaises(ValueError):

            self.client.generate_contract(
                demande,
                "autre"
            )

# test add signer:
@override_settings(
    YOUSIGN_BASE_URL="https://api-sandbox.yousign.app/v3",
    YOUSIGN_API_KEY="fake-api-key",
)
class TestYousignError(SimpleTestCase):

    @patch("apps.core.yousignservice.requests.request")
    def test_add_signer_returns_400_error(self, mock_request):

        # Simulate YouSign's HTTP 400 response
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.reason = "Bad Request"
        mock_response.json.return_value = {
            "message": "You have some invalid params in your payload."
        }

        mock_response.raise_for_status.side_effect = requests.HTTPError(
            "400 Client Error: Bad Request"
        )

        mock_request.return_value = mock_response

        client = YousignClient()

        # Check that your application raises the expected error
        with self.assertRaises(RuntimeError) as context:
            client.add_signer(
                request_id="request-123",
                document_id="document-123",
                first_name="Jean",
                last_name="Dupont",
                email="jean@example.com",
            )

        self.assertIn("400 Bad Request", str(context.exception))
        self.assertIn(
            "You have some invalid params in your payload.",
            str(context.exception),
        )
