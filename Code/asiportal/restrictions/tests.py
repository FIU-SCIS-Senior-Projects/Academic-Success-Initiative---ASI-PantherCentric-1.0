# Django
from django.test import TestCase, RequestFactory
from django.utils.crypto import get_random_string

# Local Django
from asiapp.tests.base_factory import AmbassadorUserFactory
from restrictions.models import TimeRestriction, TimeRestrictionManager
from restrictions.views import UpdateOrCreateHourLimitView


class TimeRestrictionTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = AmbassadorUserFactory()

    def test_time_created(self):
        self.assertFalse(TimeRestriction.objects.all().exists())
        req = self.factory.get('/')
        req.user = self.user
        response = UpdateOrCreateHourLimitView.as_view()(req)
        self.assertTrue(TimeRestriction.objects.all().exists())

    def test_existing_restriction_is_not_created(self):
        restr = TimeRestriction.objects.create(
                max_time = 20,
                user = self.user,
        )
        req = self.factory.get('/')
        req.user = self.user
        response = UpdateOrCreateHourLimitView.as_view()(req)
        queryset = TimeRestriction.objects.all()
        self.assertEqual(len(queryset), 1)
        self.assertEqual(restr, queryset[0])

    def test_time_can_be_updated(self):
        restr = TimeRestriction.objects.create(
                max_time = 20,
                user = self.user,
        )
        data = { 'max_time': 5 }
        req = self.factory.post('/', data)
        req.user = self.user
        response = UpdateOrCreateHourLimitView.as_view()(req)
        changed_restr = TimeRestriction.objects.all()
        self.assertEqual(changed_restr[0].max_time,5)




