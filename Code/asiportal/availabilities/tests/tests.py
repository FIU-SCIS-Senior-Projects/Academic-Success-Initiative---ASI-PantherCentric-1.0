from itertools import takewhile
from mock import patch
from datetime import time
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from django.test import TestCase
from semesters.tests.factory import SemesterFactory
from rquests.models import TutoringRequest
from courses.models import Course
from availabilities.forms import SubmitAvailabilityForm
from availabilities.models import Availability

class AvailabilityModelTests(TestCase):

    def setUp(self):
        self.a = User.objects.create(username='foo', first_name='Foo', last_name='Bar')
        self.st = time(11,0,0)
        self.et = time(12,0,0)

        self.s = SemesterFactory()
        self.ava = Availability.objects.create(ambassador = self.a, 
                                    start_time = self.st, 
                                    end_time = self.et, 
                                    day = 2,
                                    semester = self.s,
                                    )
                                    

    # we should be able to get availabilities from our user
    def test_user_has_times_on_days(self):
        self.assertTrue(
            self.a.availabilities.filter(
                start_time = self.st, 
                end_time = self.et,
                day = 2
                ))

    ##
    # we should be able to see an accurate representation of the 
    # availabilitiy.
    ##
    def test_availabilitie_are_represented_correctly(self):
        self.assertEqual(
                self.ava.__str__(),
                'Foo Bar on Tuesday from 11:00 AM - 12:00 PM'
                )

    def test_availabilitie_take_place_during_a_semester(self):
        self.assertTrue(self.s.availabilities_for_semester.all())
  # '''  
  #   This test is wrong and needs to be re-written
  #   def test_availabilities_are_aware_of_being_scheduled(self):
  #       TutoringRequest.objects.create(availability = self.ava,
  #                                   submitted_by=User.objects.create(),
  #                                   course=Course.objects.create(),
  #                                   status='B')
  #       self.assertTrue(Availability.objects.scheduled())
  #       self.assertFalse(Availability.objects.unscheduled())
  #   '''

    def test_availabilities_only_count_open_and_scheduled_requests(self):
         request = TutoringRequest.objects.create(
                                    availability = self.ava,
                                    submitted_by=User.objects.create(),
                                    course=Course.objects.create(team_leader = self.a ))
         request.status = 'C'
         request.save()
         # there should be at least one unscheduled availabilities
         self.assertTrue(Availability.objects.filter(is_scheduled=False))
         self.assertFalse(Availability.objects.filter(is_scheduled=True))

    def test_availabilities_are_unique(self):
        ava = Availability(ambassador = self.a, 
                                    start_time = self.st, 
                                    end_time = self.et, 
                                    day = 2,
                                    semester = self.s,
                                    )
        with self.assertRaises(IntegrityError):
            ava.create()

    def test_availabilities_dont_throw_exception_for_different_day(self):
        ava = Availability(ambassador = self.a, 
                                    start_time = self.st, 
                                    end_time = self.et, 
                                    day = 1,
                                    semester = self.s,)
        ava.create()
        ava = Availability(ambassador = self.a, 
                            start_time = '05:00:00', 
                            end_time = '06:00:00',
                            day = 1,
                            semester = self.s,)
        ava.create()
        self.assertEqual(Availability.objects.all().count(), 3)


    def test_exists_only_returns_true_for_same_times_and_day(self):
        ava = Availability(ambassador = self.a, 
                                    start_time = self.st, 
                                    end_time = self.et, 
                                    day = 2,
                                    semester = self.s,
                                    )
        self.assertTrue(ava.exists())
        ava = Availability(ambassador = self.a, 
                                    start_time = self.st, 
                                    end_time = self.et, 
                                    day = 1,
                                    semester = self.s,
                                    )
        self.assertFalse(ava.exists())

    def test_create_with_times_can_make_two_same_on_differnt_days(self):
        data = {
                'start_time' : '11:00:00',
                'end_time' : '16:00:00',
                'day' : 1,
                'semester' : self.s.pk,
                }
        form = SubmitAvailabilityForm(data=data)
        self.assertTrue(form.is_valid())
        Availability.create_with_times(self.a, form)
        self.assertEqual(Availability.objects.all().count(), 6)
        data['day'] = 3
        form = SubmitAvailabilityForm(data=data)
        self.assertTrue(form.is_valid())
        Availability.create_with_times(self.a, form)
        self.assertEqual(Availability.objects.all().count(), 11)
