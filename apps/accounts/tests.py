from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from unittest.mock import patch
from apps.accounts.forms.loginForm import LoginForm
from django import forms

User = get_user_model()


class RegistrationTestCase(TestCase):

    def test_registration_get(self):
        """Vérifier que la page d'inscription s'affiche."""

        response = self.client.get(
            reverse('accounts:registration')
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration.html')
        self.assertIn('form', response.context)

     
    # la registration réussie est testée avec un patch pour simuler l'envoi d'email    
    @patch('apps.accounts.views.mailactive')
    def test_registration_success(self, mock_mailactive):

        data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'TestPassword123!'
        }

        response = self.client.post(
            reverse('accounts:registration'),
            data=data
        )

        # Vérifier la redirection
        self.assertRedirects(
            response,
            reverse('accounts:success')
        )

        # Vérifier la création
        self.assertEqual(User.objects.count(), 1)

        user = User.objects.get(email='test@example.com')

        # Vérifier les informations
        self.assertEqual(user.username, 'testuser')

        # Vérifier que le compte est désactivé
        self.assertFalse(user.is_active)

        # Vérifier le hachage du mot de passe
        self.assertTrue(
            user.check_password('TestPassword123!')
        )

        # Vérifier l'envoi du mail
        mock_mailactive.assert_called_once()

    @patch('apps.accounts.views.mailactive')
    def test_registration_invalid_form(self, mock_mailactive):
        """Tester une inscription avec un formulaire invalide."""

        data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password1': 'password123',
        }

        response = self.client.post(
            reverse('accounts:registration'),
            data=data
        )

        # Le formulaire doit rester affiché
        self.assertEqual(response.status_code, 200)

        # Aucun utilisateur ne doit être créé
        self.assertEqual(User.objects.count(), 0)

        # Aucun email ne doit être envoyé
        mock_mailactive.assert_not_called()
        
# login view test cases: 
class LoginTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='TestPassword123!'
        )

        self.login_url = reverse('accounts:login')
        self.home_url = reverse('core:home')

        self.original_captcha = LoginForm.base_fields['captcha']
        LoginForm.base_fields['captcha'] = forms.CharField(required=False)

    def tearDown(self):
        LoginForm.base_fields['captcha'] = self.original_captcha
            
    def test_login_wrong_password(self):
            """Connexion avec un mauvais mot de passe."""

            data = {
                'email': 'test@example.com',
                'password': 'WrongPassword123!'
            }

            response = self.client.post(self.login_url, data)

            self.assertEqual(response.status_code, 200)
            self.assertContains(
                response,
                'Email or password is incorrect'
            )

            self.assertNotIn('_auth_user_id', self.client.session)


    def test_login_email_not_found(self):
        data = {
            'email': 'unknown@example.com',
            'password': 'TestPassword123!',
            'captcha': 'test-captcha'
        }

        response = self.client.post(self.login_url, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['error'],
            'Email or password is incorrect'
        )
  
    def test_login_inactive_user(self):
        """Connexion avec un compte désactivé."""

        self.user.is_active = False
        self.user.save()

        data = {
            'email': 'test@example.com',
            'password': 'TestPassword123!',
            'captcha': 'test-captcha'
        }

        response = self.client.post(self.login_url, data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'Your account is blocked'
        )

        self.assertNotIn('_auth_user_id', self.client.session)
        

# logout test cases:
class LogoutTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='TestPassword123!'
        )

        self.logout_url = reverse('accounts:logout')
        self.login_url = reverse('accounts:login')

    def test_logout_success(self):
        # Connecter l'utilisateur
        self.client.login(
            email='test@example.com',
            password='TestPassword123!'
        )

        # Vérifier que l'utilisateur est connecté
        self.assertIn('_auth_user_id', self.client.session)

        # Effectuer la déconnexion
        response = self.client.get(self.logout_url)

        # Vérifier la redirection vers login
        self.assertRedirects(response, self.login_url)

        # Vérifier que l'utilisateur est déconnecté
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_logout_without_login(self):
        # Déconnexion sans être connecté
        response = self.client.get(self.logout_url)

        # Vérifier la redirection
        self.assertRedirects(response, self.login_url)

        # Vérifier que personne n'est connecté
        self.assertNotIn('_auth_user_id', self.client.session)        

