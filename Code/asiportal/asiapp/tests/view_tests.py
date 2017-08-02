from mock import patch, MagicMock
from django.test import TestCase, RequestFactory
from django.template.loader import render_to_string
from django.contrib.auth.models import User, AnonymousUser
from tokens.models import AccountActivationToken
from asiapp.views import (
        HomePageView,
        LoginView,
        CreateAccountFormView,
        ActivateAccountView,
        )

class HomePageViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username='john',
                                        first_name='John',
                                        last_name='Doe',
                                        )
        self.user.set_password('password')
        self.user.save()

    def test_home_page_tells_anonymous_users_to_log_in(self):
        request = self.factory.get('/')
        request.user = AnonymousUser()
        response = HomePageView.as_view()(request)
        self.assertEqual(response.status_code, 302)

    def test_home_page_tells_logged_in_users_their_name(self):
        request = self.factory.get('/')
        request.user = self.user
        response = HomePageView.as_view()(request)
        response.render()
        name = self.user.get_full_name()
        self.assertIn(name, response.content.decode())

class LoginViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='john',
                                        first_name='John',
                                        last_name='Doe')
        self.password = 'password'
        self.user.set_password(self.password)
        self.user.save()
        self.factory = RequestFactory()

    def test_users_can_access_log_in_page(self):
        request = self.factory.get('/login')
        response = LoginView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    @patch('asiapp.views.LoginView.form_valid',
                    MagicMock(name='form_valid'))
    def test_users_are_logged_in_after_submitting_the_form(self):
        data = {'username' : self.user.username,
                'password' : self.password
                }
        request = self.factory.post('/login', data)
        response = LoginView.as_view()(request)
        self.assertTrue(LoginView.form_valid.called)
        self.assertEqual(LoginView.form_valid.call_count, 1)

class CreateAccountFormViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_url_to_view_works(self):
        request = self.client.get('/accounts/register')
        self.assertEqual(request.status_code, 200)

    def test_that_form_can_post_with_correct_data(self):
        data = {'first_name' : 'Jake',
                'last_name' : 'Lopez',
                'password1' : 'p455w0rddd111',
                'password2' : 'p455w0rddd111',
                'email' : 'passman@fiu.edu',
                }
        request = self.factory.post('/', data)
        response = CreateAccountFormView.as_view()(request)
        self.assertEqual(response.status_code, 302)

    def test_that_form_wont_post_with_incorrect_data(self):
        data = {'first_name' : 'Jake',
                'last_name' : 'Lopez',
                'password1' : 'p455w0rddd111',
                'password2' : 'p455w0rddd111',
                'email' : 'passman@gmail.edu',
                }
        request = self.factory.post('/', data)
        response = CreateAccountFormView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_that_user_created_with_data(self):
        data = {'first_name' : 'Jake',
                'last_name' : 'Lopez',
                'password1' : 'p455w0rddd111',
                'password2' : 'p455w0rddd111',
                'email' : 'passman@fiu.edu',
                }
        request = self.factory.post('/', data)
        response = CreateAccountFormView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        username = data['email'].split('@')[0]
        self.assertTrue(User.objects.get(username=username))

class ActivateAccountViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(
                is_active = False,
                first_name = 'Jake',
                last_name = 'Lopez',
                email = 'jlope590@fiu.edu',
                )
        self.user.set_password('dickyballs')
        self.user.save()
        self.tok = AccountActivationToken.objects.create(user=self.user)

    def test_that_user_can_log_in_after_account_is_vallid(self):
        data = { }
        self.assertFalse(self.tok.used)
        self.assertFalse(self.user.is_active)
        request = self.factory.post('/', data)
        kwargs = { 'token' : self.tok.token }
        response = ActivateAccountView.as_view()(request, **kwargs) 
        self.assertEqual(response.status_code, 302)
        user = User.objects.get()
        self.assertTrue(user.is_active)
        login = self.client.login(username=user.username,
                password='dickyballs')
        token = AccountActivationToken.objects.get()
        self.assertTrue(token.used)
        self.assertTrue(login)
