from datetime import time
from unittest import skip
from django.test import TestCase
from availabilities.forms import SubmitAvailabilityForm
from semesters.models import Semester

class SubmitAvailabilityFormTest(TestCase):

    def test_form_can_be_valid(self):
        semester = Semester.objects.create()
        data = {'start_time' : '11:00:00',
                'end_time' : '12:00:00',
                'day' : 1,
                'semester' : semester.pk,
                }
        form = SubmitAvailabilityForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_accepts_12hr_time(self):
        semester = Semester.objects.create()
        data = {'start_time' : '12:00 am',
                'end_time' : '1:00 pm',
                'day' : 1,
                'semester' : semester.pk,
                }
        form = SubmitAvailabilityForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_checks_that_times_are_valid(self):
        semester = Semester.objects.create()
        expctd_msg = 'Please make sure these times are correct.'
        data = {'start_time' : '2:00 pm',
                'end_time' : '1:00 pm',
                'day' : 1,
                'semester' : semester.pk,
                }
        form = SubmitAvailabilityForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn(expctd_msg,form._errors['start_time'])
        self.assertIn(expctd_msg,form._errors['end_time'])

    def test_form_chops_up_time_intervals(self):
        semester = Semester.objects.create()
        expctd_msg = 'Please make sure these times are correct.'
        data = {'start_time' : '2:00 pm',
                'end_time' : '5:00 pm',
                'day' : 1,
                'semester' : semester.pk,
                }
        expected_result = [time(14,0,0),
                time(15,0,0),
                time(16,0,0),
                time(17,0,0),]
        form = SubmitAvailabilityForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(expected_result, form._times)
