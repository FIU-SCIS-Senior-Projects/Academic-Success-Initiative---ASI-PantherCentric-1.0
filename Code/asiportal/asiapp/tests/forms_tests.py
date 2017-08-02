from django.contrib.auth.models import User
from django.test import TestCase
from asiapp.forms import LogInForm, CreateAccountForm

class LogInFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='john')
        self.password = 'password'
        self.user.set_password(self.password)
        self.user.save()

    def test_form_can_be_valid(self):
        data = {'username' : self.user.username,
                'password' : self.password
                }
        form = LogInForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_needs_a_password(self):
        data = {'username' : self.user.username,
                }
        form = LogInForm(data=data)
        expected_error = 'This field is required.'
        self.assertFalse(form.is_valid())
        self.assertIn(expected_error, form.errors['password'])

    def test_form_invalid_with_nonexistant_user(self):
        data = {'username' : 'chungo',
                'password' : 'spuddyballman'
                }
        form = LogInForm(data=data)
        self.assertFalse(form.is_valid())

class CreateAccountFormTests(TestCase):

    def test_form_needs_first_name_to_be_valid(self):
        data = { 'last_name' : 'Lopez',
                'password1' : 'p4510aa2322!!',
                'password2' : 'p4510aa2322!!',
                'email' : 'passman@gmail.com',
                }
        form = CreateAccountForm(data=data)
        self.assertFalse(form.is_valid())

    def test_form_needs_last_name_to_be_valid(self):
        data = { 'first_name' : 'Jake',
                'password1' : 'p4510aa2322!!',
                'password2' : 'p4510aa2322!!',
                'email' : 'passman@fiu.edu',
                }
        form = CreateAccountForm(data=data)
        self.assertFalse(form.is_valid())


    def test_non_fiu_emails_are_invalid(self):
        data = {'first_name' : 'Jake',
                'last_name' : 'Lopez',
                'email' : 'woogyboogy@gmail.com',
                'password1' : 'p4510aa2322!!',
                'password2' : 'p4510aa2322!!',
                }
        form = CreateAccountForm(data=data)
        self.assertFalse(form.is_valid())

    def test_form_can_be_valid(self):
        data = {'first_name' : 'Jake',
                'last_name' : 'Lopez',
                'password1' : 'p4510aa2322!!',
                'password2' : 'p4510aa2322!!',
                'email' : 'passman@fiu.edu',
                }
        form = CreateAccountForm(data=data)
        self.assertTrue(form.is_valid())

    def test_when_form_is_saved_a_user_is_created(self):
        data = {
                'first_name' : 'Jake',
                'last_name' : 'Lopez',
                'password1' : 'p4510aa2322!!',
                'password2' : 'p4510aa2322!!',
                'email' : 'Passman@fiu.edu',
                }
        username = data['email'].split('@')[0]
        form = CreateAccountForm(data=data)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertTrue(User.objects.all())
        user = User.objects.get(first_name=data['first_name'])
        self.assertEqual(user.first_name, data['first_name'])
        self.assertEqual(user.last_name, data['last_name'])
        self.assertEqual(user.email, data['email'])
        self.assertNotEqual(user.username, username)
        self.assertEqual(user.username, username.lower())
        self.assertFalse(user.is_active)

