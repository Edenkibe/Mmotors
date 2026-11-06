from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

from apps.voiture.models import Voiture
from apps.dossiers.form.dossierForm import DossierAchatForm
from apps.dossiers.models import DossierAchat
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()


class DepotDossierTest(TestCase):

    def setUp(self):
        self.client = Client()

        # Créer un utilisateur
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )

        # Connecter l'utilisateur
        self.client.force_login(self.user)

        # Créer une voiture
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

        # URL de la vue
        self.url = reverse(
            "dossiers:depot_dossier",
            kwargs={"id": self.car.id}
        )

    def test_depot_dossier_get(self):
        """Vérifier que la page s'affiche correctement."""

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "depot_dossier.html")
        self.assertIsInstance(response.context["form"], DossierAchatForm)
        self.assertEqual(response.context["get_car"], self.car)


    def test_depot_dossier_car_not_found(self):
        """Vérifier le comportement si la voiture n'existe pas."""

        url = reverse(
            "dossiers:depot_dossier",
            kwargs={"id": 999999}
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_depot_dossier_post_valid(self):
        """Vérifier la création d'un dossier avec des données valides."""

        fichier = SimpleUploadedFile(
                "piece_identite.pdf",
                b"Contenu fictif du document PDF",
                content_type="application/pdf"
            )
        
        data = {
            "nom_complet": "John Doe",
            "telephone": "1234567890",
            "email": "john.doe@example.com",
            "adresse": "123 Main St",
            "piece_identite": fichier
        }

        response = self.client.post(self.url, data)

        print("ERREURS :", response.context["form"].errors
            if response.context and response.context.get("form")
            else "Aucune erreur")

        self.assertEqual(response.status_code, 302)

        self.assertRedirects(
            response,
            reverse("dossiers:success_dossier_depot")
        )

        self.assertEqual(DossierAchat.objects.count(), 1)

        dossier = DossierAchat.objects.first()

        self.assertEqual(dossier.client, self.user)
        self.assertEqual(dossier.vehicule, self.car)
        
# test sur la recherche de dossier par code_dossier:
class SearchDossierTest(TestCase):

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

        self.dossier1 = DossierAchat.objects.create(
            code_dossier="DOSSIER001",
            nom_complet="Pierre Martin",
            telephone="06 11 22 33 44",
            adresse="789 Boulevard Saint-Germain",
            email="pierre.martin@example.com",
            piece_identite="Passeport",
            client=self.user,
            vehicule=self.car1
        )

        self.dossier2 = DossierAchat.objects.create(
            code_dossier="DOSSIER002",
            nom_complet="Jean Dupont",
            telephone="06 12 34 56 78",
            adresse="123 Rue de la Paix",
            email="jean.dupont@example.com",
            piece_identite="Passeport",
            client=self.user,
            vehicule=self.car1
        )

        self.dossier3 = DossierAchat.objects.create(
            code_dossier="ABC123",
            nom_complet="Marie Curie",
            telephone="06 98 76 54 32",
            adresse="456 Avenue des Champs-Élysées",
            email="marie.curie@example.com",
            piece_identite="Carte d'identité",
            client=self.user,
            vehicule=self.car1
        )

        self.url = reverse("dossiers:search_dossier")

    def test_search_dossier_empty_query(self):
        """Vérifier que tous les dossiers sont retournés si la recherche est vide."""

        response = self.client.get(self.url, {"q": ""})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["query"], "")
        self.assertEqual(response.context["total"], 3)
        self.assertEqual(response.context["dossier_user"].count(), 3)

    def test_search_dossier_valid_query(self):
        """Vérifier la recherche par code de dossier."""

        response = self.client.get(self.url, {"q": "DOSSIER001"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total"], 1)

        dossier = response.context["dossier_user"].first()

        self.assertEqual(dossier.code_dossier, "DOSSIER001")

    def test_search_dossier_partial_query(self):
        """Vérifier la recherche avec une partie du code."""

        response = self.client.get(self.url, {"q": "DOSSIER"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total"], 2)

    def test_search_dossier_short_query(self):
        """Vérifier qu'une recherche de moins de 2 caractères ne retourne rien."""

        response = self.client.get(self.url, {"q": "D"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total"], 0)
        self.assertEqual(response.context["dossier_user"].count(), 0)

    def test_search_dossier_no_result(self):
        """Vérifier le comportement lorsqu'aucun dossier ne correspond."""

        response = self.client.get(self.url, {"q": "INEXISTANT"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total"], 0)

    def test_search_dossier_query_with_spaces(self):
        """Vérifier que les espaces autour de la recherche sont supprimés."""

        response = self.client.get(self.url, {"q": " DOSSIER001 "})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["query"], "DOSSIER001")
        self.assertEqual(response.context["total"], 1)

    def test_search_dossier_ajax(self):
        """Vérifier le template utilisé pour une requête AJAX."""

        response = self.client.get(
            self.url,
            {"q": "DOSSIER"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(
            response,
            "admin_template/partials/all_demande_ajax.html"
        )

        self.assertEqual(response.context["total"], 2)      

#test sur la recherche de  voiture acheter:         
class SearchSoldCarTest(TestCase):

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
               marque="BMW X5",
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
        self.car3= Voiture.objects.create(
                marque="Tesla Model S",
                type="Achat",
                disponibilite="Invisible",
                modele="Model S",
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
        )
   
        self.dossier2 = DossierAchat.objects.create(
               code_dossier="DOSSIER002",
               nom_complet="Jean Dupont",
               telephone="06 12 34 56 78",
               adresse="123 Rue de la Paix",
               email="jean.dupont@example.com",
               piece_identite="Passeport",
               client=self.user,
               vehicule=self.car2,
               deal="acheté",
        )
   
        self.dossier3 = DossierAchat.objects.create(
            code_dossier="ABC123",
            nom_complet="Marie Curie",
            telephone="06 98 76 54 32",
            adresse="456 Avenue des Champs-Élysées",
            email="marie.curie@example.com",
            piece_identite="Carte d'identité",
            client=self.user,
            vehicule=self.car3,
            deal="en attente",
        )
        self.url = reverse("dossiers:search_sold_car")
        
        print("\n===== TEST DATA =====")

        for dossier in DossierAchat.objects.all():
            print(
                dossier.code_dossier,
                dossier.deal,
                dossier.vehicule.marque,
                dossier.vehicule.modele
            )

        print("=====================\n")

    def test_search_sold_car_empty_query(self):
        """Vérifier que tous les véhicules achetés sont retournés."""

        response = self.client.get(self.url, {"q": ""})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["sold_car"]), 2)
        self.assertEqual(response.context["total"], 2)

    def test_search_sold_car_valid_query(self):
        """Vérifier la recherche par code de dossier."""

        response = self.client.get(
            self.url, {"q": "DOSSIER001"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["sold_car"]), 1)
        self.assertEqual(
            response.context["sold_car"].first(),
            self.dossier1,
        )

    def test_search_sold_car_search_by_brand(self):
        """Vérifier la recherche par marque."""

        response = self.client.get(self.url, {"q": "Toyota"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["sold_car"]), 1)
        self.assertEqual(
            response.context["sold_car"].first(),
            self.dossier1,
        )

    def test_search_sold_car_search_by_model(self):
        """Vérifier la recherche par modèle."""

        response = self.client.get(self.url, {"q": "Corolla"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["sold_car"]), 1)

    def test_search_sold_car_short_query(self):
        """Vérifier qu'une recherche de moins de 2 caractères ne retourne rien."""

        response = self.client.get(self.url, {"q": "T"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["sold_car"]), 0)

    def test_search_sold_car_no_result(self):
        """Vérifier le comportement lorsqu'aucun résultat ne correspond."""

        response = self.client.get(
            self.url, {"q": "INEXISTANT"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["sold_car"]), 0)

    def test_search_sold_car_query_with_spaces(self):
        """Vérifier que les espaces autour de la recherche sont supprimés."""

        response = self.client.get(
            self.url, {"q": " DOSSIER001 "}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["sold_car"]), 1)          