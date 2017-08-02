from datetime import timedelta
from django.test import TestCase, RequestFactory
from django.utils import timezone
from django.contrib.auth.models import User
from tutoring_sessions.models import Session, IndividualSession
from availabilities.models import Availability
from tutoring_sessions.views import (
        TutoringSessionUpdateView,
        TutoringSessionListView)
from courses.models import Course
from semesters.models import Semester

class CommonSetUp(TestCase):
    def setUp(self):
        self.sem = Semester.objects.create(
                start_date=timezone.now(),
                end_date=timezone.now()+timedelta(weeks=12),
                )
        self.cou = Course.objects.create(name='MAC2312')
        self.amb1 = User.objects.create(username='amb1')
        self.cou.team_leader = self.amb1
        self.cou.save()
        self.tut = User.objects.create(username='tut')
        self.factory = RequestFactory()
        self.ava = Availability.objects.create(
                ambassador = self.amb1,
                start_time = '13:00:00',
                end_time = '13:00:00',
                day=1,
                semester = self.sem
                )
        self.sess = Session.objects.create(
                ambassador = self.amb1,
                start_time = self.ava.start_time,
                end_time = self.ava.end_time,
                day_of_week = self.ava.day,
                availability = self.ava,
                tutee = self.tut,
                course = self.cou,
                start_date = timezone.now(),
                end_date = timezone.now() + timedelta(weeks=12),
                )
        days = self.sess.get_dates()
        IndividualSession.make_from_dates(self.sess, days)

class TutoringSessionListViewTest(CommonSetUp):
    def test_that_sessions_can_be_seen(self):
        request = self.factory.get('/')
        request.user = self.amb1
        response = TutoringSessionListView.as_view()(request)
        sessions = response.context_data['object_list']
        self.assertTrue(sessions)
        self.assertIn(self.sess, sessions)
    def test_that_other_users_sessions_cant_be_seen(self):
        request = self.factory.get('/')
        request.user = User.objects.create(username='amb2')
        response = TutoringSessionListView.as_view()(request)
        sessions = response.context_data['object_list']
        self.assertFalse(sessions)
        self.assertNotIn(self.sess, sessions)

class TutoringSessionUpdateViewTests(CommonSetUp):
    def test_that_sessions_can_be_updated(self):
        new_ambassador = User.objects.create(username='amb2')
        kwargs = { 'pk' : self.sess.pk }
        data = {
                'ambassador' : new_ambassador.pk,
                'start_date' : timezone.now().date(),
                }
        request = self.factory.post('/', data)
        response = TutoringSessionUpdateView.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)
        session = Session.objects.filter(
                availability__ambassador=new_ambassador
                )
        individual_sessions = IndividualSession.objects.filter(
                session__availability__ambassador=new_ambassador,)
        self.assertTrue(session)
        self.assertTrue(individual_sessions)
