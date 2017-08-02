from datetime import timedelta
import mock
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.urlresolvers import reverse_lazy
from django.db import transaction
from django.test import TestCase, RequestFactory
from django.template.loader import render_to_string
from availabilities.views import (SubmitAvailabilityFormView,
                                  AvailabilityListView,
                                  AvailabilityUpdateView,
                                  AvailabilityDeleteView)
from availabilities.forms import SubmitAvailabilityForm
from semesters.models import Semester
from availabilities.models import Availability

def setup_view(view, request, *args, **kwargs):
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view

class SubmitAvailabilityFormViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username='foo')
        self.user.set_password('bar')
        self.user.save()
        self.semester = Semester.objects.create()

    def test_that_view_can_be_called(self):
        request = self.factory.get('/')
        response = SubmitAvailabilityFormView.as_view()(request)
        self.assertTrue(response.status_code, 200)

    def test_that_templates_are_returned(self):
        request = self.factory.get('/')
        view = setup_view(SubmitAvailabilityFormView, request)
        template_names = view.get_template_names(view)
        expected_names = ['availabilities/submit_form.html']
        self.assertTrue(template_names)
        self.assertEqual(template_names, expected_names)

    def test_that_availabilities_can_be_made(self):
        data = {
                'start_time' : '11:00:00',
                'end_time' : '12:00:00',
                'day' : 1,
                'semester' : self.semester.pk,
                }
        request = self.factory.post('/availabilities', data)
        request.user = self.user
        response = SubmitAvailabilityFormView.as_view()(request)
        self.assertTrue(Availability.objects.\
                filter(start_time=data['start_time'],
                    end_time=data['end_time'],
                    day=data['day'],
                    semester=data['semester'],
                    ))
        self.assertEqual(response.status_code, 302)

    def test_that_availabilities_can_be_made_with_chunks(self):
        data = {
                'start_time' : '11:00:00',
                'end_time' : '16:00:00',
                'day' : 1,
                'semester' : self.semester.pk,
                }
        request = self.factory.post('/availabilities', data)
        request.user = self.user
        response = SubmitAvailabilityFormView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Availability.objects.all().count(), 5)
        avas = Availability.objects.all()
        self.assertTrue(avas.filter(start_time=data['start_time'], 
            end_time='12:00:00'))
        self.assertTrue(avas.filter(start_time='15:00:00', 
            end_time=data['end_time']))
        self.assertFalse(avas.filter(start_time=data['start_time'],
            end_time=data['end_time']))

    # pending
    def test_that_summer_c_availabilities_make_summer_a_and_b(self):
        sum_c = Semester.objects.create(term='SC')

        sum_a = Semester.objects.create(term='SA',
                start_date = sum_c.start_date,
                end_date = sum_c.start_date + timedelta(weeks=6))

        sum_b = Semester.objects.create(term='SB',
                start_date = sum_a.end_date,
                end_date = sum_c.end_date)

        data = {
                'start_time' : '11:00:00',
                'end_time' : '12:00:00',
                'day' : 1,
                'semester' : sum_c.pk,
                }
        request = self.factory.post('/availabilities', data)
        request.user = self.user
        response = SubmitAvailabilityFormView.as_view()(request)
        a = Availability.objects.all()
        self.assertTrue(a.filter(start_time=data['start_time'],
                    end_time=data['end_time'],
                    day=data['day'],
                    semester=data['semester'],
                    ))
        self.assertEqual(a.count(), 3)
        self.assertTrue(a.filter(semester=sum_a,
            start_time=data['start_time']))
        self.assertTrue(a.filter(semester=sum_b,
            start_time=data['start_time']))
        self.assertTrue(a.filter(semester=sum_c,
            start_time=data['start_time']))
        self.assertEqual(response.status_code, 302)

    def test_cant_submit_duplicate_availabilities(self):
        data = {
                'start_time' : '11:00:00',
                'end_time' : '16:00:00',
                'day' : 1,
                'semester' : self.semester.pk,
                }
        request = self.factory.post('/availabilities', data)
        request.user = self.user
        response = SubmitAvailabilityFormView.as_view()(request)
        request = self.factory.post('/availabilities', data)
        # do it again
        request = self.factory.post('/availabilities', data)
        request.user = self.user
        response = SubmitAvailabilityFormView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_can_submit_duplicate_times_on_different_day_(self):
        data = {
                'start_time' : '11:00:00',
                'end_time' : '16:00:00',
                'day' : 1,
                'semester' : self.semester.pk,
                }
        request = self.factory.post('/availabilities', data)
        request.user = self.user
        response = SubmitAvailabilityFormView.as_view()(request)
        request = self.factory.post('/availabilities', data)
        data2 = {
                'start_time' : '11:00:00',
                'end_time' : '16:00:00',
                'day' : 2,
                'semester' : self.semester.pk,
                }
        request = self.factory.post('/availabilities', data2)
        request.user = self.user
        response = SubmitAvailabilityFormView.as_view()(request)
        self.assertEqual(response.status_code, 302)

class AvailabilityListViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username='foo')

    def test_that_view_can_be_visited(self):
        request = self.factory.get(reverse_lazy('availabilities:list'))
        request.user = self.user
        response = AvailabilityListView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_that_availabilities_can_be_seen_only_by_the_user(self):
        sem = Semester.objects.create()
        a = Availability.objects.create(ambassador=self.user,
                start_time='11:00:00',
                end_time='12:00:00',
                semester=sem)
        request = self.factory.get('/')
        request.user = self.user
        view = AvailabilityListView()
        view = setup_view(view, request) 
        self.assertIn(a, view.get_queryset())

    def test_that_availabilities_cant_be_seen_by_others(self):
        new_guy = User.objects.create(username='bar')
        sem = Semester.objects.create()
        a = Availability.objects.create(ambassador=self.user,
                start_time='11:00:00',
                end_time='12:00:00',
                semester=sem)
        request = self.factory.get('/')
        request.user = new_guy
        view = AvailabilityListView()
        view = setup_view(view, request) 
        self.assertNotIn(a, view.get_queryset())

class AvailabilityUpdateViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username='Foo')
        self.sem = Semester.objects.create()
        self.ava = Availability.objects.create(ambassador=self.user,
                start_time='11:00:00',
                end_time='12:00:00',
                semester=self.sem)

    def test_that_view_is_visitable(self):
        kwargs = {'pk' : self.ava.pk}
        request = self.factory.get(reverse_lazy('availabilities:edit',
            kwargs=kwargs))
        response = AvailabilityUpdateView.as_view()(request, pk=self.ava.pk)
        self.assertEqual(response.status_code, 200)

    def test_that_availabilities_can_be_updated(self):
        kwargs = {'pk' : self.ava.pk}
        data = { 'start_time' : '13:00:00',
                'end_time' : '14:00:00',
                'semester' : self.ava.semester.pk,
                'day' : self.ava.day,
                }
        request = self.factory.post(reverse_lazy('availabilities:edit',
            kwargs=kwargs), data)
        request.user = self.ava.ambassador
        response = AvailabilityUpdateView.as_view()(request, pk=self.ava.pk)
        self.assertEqual(response.status_code, 302)

    def test_that_availabilities_cant_be_updated_with_existing_times(self):
        kwargs = {'pk' : self.ava.pk}
        data = { 'start_time' : '13:00:00',
                'end_time' : '14:00:00',
                'semester' : self.ava.semester.pk,
                'day' : self.ava.day,
                }
        Availability.objects.create(
                start_time=data['start_time'],
                end_time=data['end_time'],
                semester=self.ava.semester,
                day=data['day'],
                ambassador=self.ava.ambassador,)
        request = self.factory.post(reverse_lazy('availabilities:edit',
            kwargs=kwargs), data)
        request.user = self.ava.ambassador
        response = AvailabilityUpdateView.as_view()(request, pk=self.ava.pk)
        self.assertEqual(response.status_code, 200)

    def test_that_availabilities_can_be_deleted(self):
        kwargs = {'pk' : self.ava.pk}
        data = { 'start_time' : '13:00:00',
                'end_time' : '14:00:00',
                'semester' : self.ava.semester.pk,
                'day' : self.ava.day,
                }
        request = self.factory.post(reverse_lazy('availabilities:edit',
            kwargs=kwargs), data)
        response = AvailabilityDeleteView.as_view()(request, pk=kwargs.get('pk'))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Availability.objects.all())
