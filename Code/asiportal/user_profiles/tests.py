from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from .views import (
        UserProfileCreateView,
        UserProfileDetailView,
        UserProfileUpdateView,
        )
from .models import UserProfile

# Create your tests here.

class CommonCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='john',
                first_name='John',
                last_name='Doe',)
        self.user.save()
        self.factory = RequestFactory()

class UserProfileCreateViewTests(CommonCase):

    def test_authed_user_can_view_page(self):
        request = self.factory.get('garbage')
        request.user = self.user
        response = UserProfileCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_profiles_can_be_created(self):
        post_data = {
                'sex': 'F',
                'major' : 'CS',
                'phone_number' : '3053053005',
                }
        request = self.factory.post('garbage', data=post_data)
        request.user = self.user
        response = UserProfileCreateView.as_view()(request)
        self.assertTrue(UserProfile.objects.all())
        self.assertEqual(response.status_code, 302)

class UserProfileDetailViewTest(CommonCase):

    def setUp(self):
        super(UserProfileDetailViewTest, self).setUp()
        self.profile = UserProfile.objects.create(
                user = self.user,
                major = 'CS',
                sex = 'M',
                phone_number = '3053053005',
                )

    def test_profiles_can_be_viewed_by_user(self):
        kwargs = {
                'pk' : self.user.pk
                }
        request = self.factory.get('garbage', kwargs=kwargs)
        request.user = self.user
        response = UserProfileDetailView.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 200)

    def test_users_with_no_profile_get_instructed_to_create_one(self):
        u2 = User.objects.create(username='jane',
                first_name = 'Jane',
                last_name = 'Doe',
                )
        kwargs = {
                'pk' : u2
                }
        request = self.factory.get('garbage', kwargs=kwargs)
        request.user = u2
        response = UserProfileDetailView.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 200)

class UserProfileUpdateViewTest(CommonCase):
    def setUp(self):
        super(UserProfileUpdateViewTest, self).setUp()
        self.profile = UserProfile.objects.create(
                user = self.user,
                major = 'CS',
                sex = 'M',
                phone_number = '3053053005',
                )

    def test_user_can_update_profile(self):
        post_data = {
                'major' : 'IT',
                'sex' : 'M',
                'phone_number' : '3053333333',
        }
        kwargs = { 'pk' : self.profile.pk }
        request = self.factory.post('garbage', data=post_data)
        request.user = self.user
        response = UserProfileUpdateView.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)
        updated_profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(updated_profile.sex, post_data['sex'])
        self.assertEqual(updated_profile.major, post_data['major'])
        self.assertEqual(updated_profile.phone_number, post_data['phone_number'])

    def test_user_can_only_update_their_profile(self):
        u2 = User.objects.create(
                username='jane',
                first_name='Jane',
                last_name='Doe')
        kwargs = { 'pk' : self.profile.pk }
        request = self.factory.get('garbage')
        request.user = u2
        response = UserProfileUpdateView.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)
