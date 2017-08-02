from django.test import TestCase
from django.contrib.auth.models import User
from availabilities.tests.factory import AvailabilityFactory
from rquests.models import TutoringRequest
from courses.models import Course
from semesters.models import Semester

class TutoringRequestTest(TestCase):
    def setUp(self):
        self.amb = User.objects.create(username='bar',
                                      first_name='John',
                                      last_name='Doe')
        self.stu = User.objects.create(username='foo',
                                      first_name='Jane',
                                      last_name='Doe',)
        self.sem = Semester.objects.create()
        self.ava = AvailabilityFactory(ambassador=self.amb,
                                       semester=self.sem)
        self.cou = Course.objects.create(name='MAC2311', team_leader=self.amb)

    def test_requests_are_submitted_by_users_for_with_an_availability(self):
        TutoringRequest.objects.create(submitted_by=self.stu,
                                       availability = self.ava,
                                       course=self.cou)
        self.assertTrue(self.ava.requests.filter(submitted_by=self.stu))


    def test_requests_are_timestamped_when_submitted(self):
        t = TutoringRequest.objects.create(submitted_by=self.stu,
                                       availability = self.ava,
                                       course=self.cou)
        self.assertTrue(t.submitted_at)

    def test_requests_timestamped_dont_overwrite(self):
        t = TutoringRequest.objects.create(submitted_by=self.stu,
                                       availability = self.ava,
                                       course = self.cou,)
        expected = t.submitted_at
        t.save()
        self.assertEqual(t.submitted_at, expected)

    def test_requests_can_be_updated(self):
        t = TutoringRequest.objects.create(submitted_by=self.stu,
                                       availability = self.ava,
                                       course = self.cou,)
        t.status = 'B'
        t.save()
        self.assertEqual(t.get_status_display(), 'Scheduled')

    def test_requests_when_updated_get_timestamped(self):
        t = TutoringRequest.objects.create(submitted_by=self.stu,
                                       availability = self.ava,
                                       course = self.cou,)
        t.status = 'B'
        t.save()
        self.assertTrue(t.updated_at)

    def test_requests_are_represented_correctly(self):
        t = TutoringRequest.objects.create(submitted_by=self.stu,
                                       availability = self.ava,
                                       course = self.cou,)
        expected_text = '%s with %s from %s' % (t.course,
                                           t.availability, 
                                           t.submitted_by.get_full_name())
        self.assertEqual(t.__str__(), expected_text)
