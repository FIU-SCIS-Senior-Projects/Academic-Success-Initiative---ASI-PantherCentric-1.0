from django.contrib.auth.models import User
from django.test import TestCase
from availabilities.tests.factory import AvailabilityFactory
from courses.models import Course
from rquests.forms import (RequestTutoringForm,
                UpdateTutoringRequestForm)
from rquests.models import TutoringRequest
from semesters.models import Semester
from restrictions.models import TimeRestriction

class RequestTutoringFormTest(TestCase):
    def setUp(self):
        self.sem = Semester.objects.create()
        self.amb = User.objects.create(username='john',
                                       first_name='John',
                                       last_name='Doe')
        self.ava = AvailabilityFactory(ambassador=self.amb,
                                       semester=self.sem)
        self.course = Course.objects.create(name='MAC2311', team_leader=self.amb)
        self.course.team.add(self.amb)
        self.kwargs = {'course' : self.course.slug,
                        'semester' : self.sem.slug}

    def test_form_invalid_with_wrong_data(self):
        data = {}
        form = RequestTutoringForm(data=data, **self.kwargs)
        self.assertFalse(form.is_valid())

    def test_unrelated_availabiltiies_not_in_form_queryset(self):
        amb = User.objects.create(username='Teem')
        ava = AvailabilityFactory(ambassador=amb,
                                  semester=self.sem)
        form = RequestTutoringForm(**self.kwargs)
        queryset = form.fields['availability'].queryset
        self.assertNotIn(ava, queryset)

    def test_availability_in_form_queryset(self):
        form = RequestTutoringForm(**self.kwargs)
        queryset = form.fields['availability'].queryset
        self.assertIn(self.ava, queryset)

    def test_form_valid_with_right_data(self):
        data = { 'availability' : self.ava.id }
        form = RequestTutoringForm(data=data, **self.kwargs)
        self.assertTrue(form.is_valid())

    def test_form_only_shows_availabilities_for_current_semester(self):
        sem = Semester.objects.create(year=1852) 
        self.kwargs['semester'] = sem.slug
        form = RequestTutoringForm(**self.kwargs)
        self.assertFalse(form.fields['availability'].queryset)

    def test_form_shows_availabilities_from_current_semester(self):
        sem = Semester.objects.create()
        self.kwargs['semester'] = sem.slug
        ava = AvailabilityFactory(semester=sem,
                                  ambassador=self.amb)
        form = RequestTutoringForm(**self.kwargs)
        self.assertTrue(form.fields['availability'].queryset)

    def test_form_shows_only_unscheduled_availabilities(self):
        dupy = self.ava
        dupy.is_scheduled = True
        dupy.save()
        tr = TutoringRequest.objects.create(availability=dupy,
                                            submitted_by=self.amb,
                                            course=self.course)
        form = RequestTutoringForm(**self.kwargs)
        self.assertNotIn(self.ava, form.fields['availability'].queryset)

    def test_form_doesnt_show_ambassadors_with_time_restrictions(self):
        special_guy = User.objects.create(username='SpecialGuy')
        tr = TimeRestriction.objects.create(user = special_guy,
                                            max_time=0)
        self.course.team.add(special_guy)
        avail = AvailabilityFactory(ambassador=special_guy,
                                       semester=self.sem)
        form = RequestTutoringForm(**self.kwargs)
        self.assertNotIn(avail, form.fields['availability'].queryset)

class UpdateTutoringRequestFormTest(TestCase):
    def setUp(self):
        self.sem = Semester.objects.create()
        self.amb = User.objects.create(username='john',
                                       first_name='John',
                                       last_name='Doe')
        self.ava = AvailabilityFactory(ambassador=self.amb,
                                       semester=self.sem)
        self.course = Course.objects.create(name='MAC2311', team_leader=self.amb)
        self.course.team.add(self.amb)
        self.tr = TutoringRequest.objects.create(availability=self.ava,
                                            submitted_by=self.amb,
                                            course=self.course)

    def test_form_is_valid_with_a_request_status_and_room(self):
        data = {'status' : 'C',
                'room_number': '101A'}
        form = UpdateTutoringRequestForm(instance=self.tr, data=data)
        self.assertTrue(form.is_valid())

    def test_form_invald_without_proper_data(self):
        form = UpdateTutoringRequestForm(instance=self.tr,)
        self.assertFalse(form.is_valid())
