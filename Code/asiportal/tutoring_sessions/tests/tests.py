from datetime import date, datetime, timedelta
import pytz
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from availabilities.models import Availability
from availabilities.tests.factory import AvailabilityFactory
from courses.models import Course
from asiapp.tests.base_factory import TuteeUserFactory
from asiapp.tests.base_factory import AmbassadorUserFactory
from semesters.models import Semester
from semesters.tests.factory import SemesterFactory
from rquests.models import TutoringRequest
from tutoring_sessions.forms import TutoringSessionUpdateForm
from tutoring_sessions.models import (Session,
        Session,
        IndividualSession)

class SessionSetUp(TestCase):
    def setUp(self):
        aware_times = pytz.utc.localize(datetime(2016,5,5))
        self.tut = User.objects.create(username='tuttee')
        self.amb = User.objects.create(username='amb')
        self.session = Session()
        self.semester = Semester.objects.create(start_date=date(2016,5,5),
                                           end_date=date(2016,6,6))
        self.av = Availability.objects.create(ambassador=self.amb,
                                         start_time='11:00:00',
                                         end_time='12:00:00',
                                         semester=self.semester,)


        course = Course.objects.create(name='MAC2311', team_leader = self.amb)
        self.tr = TutoringRequest.objects.create(submitted_by=self.tut,
                                            availability=self.av,
                                            course=course,
                                            submitted_at=aware_times,
                                            updated_at=aware_times,
                                            )

class SessionMethodsTest(SessionSetUp):
    def test_session_start_a_week_later_if_less_than_48_hours(self):
        aware_times = pytz.utc.localize(datetime(2016,5,9))
        thistr = self.tr
        av = Availability.objects.create(ambassador=self.amb,
                                         start_time='11:00:00',
                                         day=2,
                                         end_time='12:00:00',
                                         semester=self.semester,)
        thistr.updated_at = aware_times
        thistr.availability = av
        thistr.save()
        dates = Session.make_dates(thistr)
        expected_start_date = date(2016,5,17)
        expected_end_date = date(2016,5,24)
        self.assertEqual(expected_start_date, dates[0])
        self.assertEqual(expected_end_date, dates[-1])
    
    def test_session_start_a_week_later_if_date_passed(self):
        aware_times = pytz.utc.localize(datetime(2016,5,11))
        thistr = self.tr
        av = Availability.objects.create(ambassador=self.amb,
                                         start_time='11:00:00',
                                         day=2,
                                         end_time='12:00:00',
                                         semester=self.semester,)
        thistr.updated_at = aware_times
        thistr.availability = av
        thistr.save()
        dates = Session.make_dates(thistr)
        expected_start_date = date(2016,5,17)
        expected_end_date = date(2016,5,24)
        self.assertEqual(expected_start_date, dates[0])
        self.assertEqual(expected_end_date, dates[-1])

    def test_session_start_a_week_later_if_updated_on_sunday_for_day_on_monday(self):
        thistr = self.tr
        aware_times = pytz.utc.localize(datetime(2016,5,15))
        thistr.updated_at = aware_times
        thistr.save()
        dates = Session.make_dates(thistr)
        expected_start_date = date(2016,5,23)
        expected_end_date = date(2016,5,30)
        self.assertEqual(expected_start_date, dates[0])
        self.assertEqual(expected_end_date, dates[-1])

    def test_session_starts_this_week_if_more_than_48_hours(self):
        thistr = self.tr
        aware_times = pytz.utc.localize(datetime(2016,5,9))
        av = Availability.objects.create(ambassador=self.amb,
                                         start_time='11:00:00',
                                         day=3,
                                         end_time='12:00:00',
                                         semester=self.semester,)
        thistr.updated_at = aware_times
        thistr.availability = av
        thistr.save()
        dates = Session.make_dates(thistr)
        expected_start_date = date(2016,5,11)
        expected_end_date = date(2016,5,25)
        self.assertEqual(expected_start_date, dates[0])
        self.assertEqual(expected_end_date, dates[-1])

    def test_session_starts_on_soonest_day_if_before_semester(self):
        before_semester = self.semester.start_date + timedelta(weeks= -1)
        self.tr.updated_at = before_semester
        dates = Session.make_dates(self.tr)
        expected_end_date = date(2016,5,30)
        expected_start_date = date(2016,5,9)
        self.assertEqual(expected_end_date, dates[-1])
        self.assertEqual(expected_start_date, dates[0])

    def test_date_correct_when_updated_at_is_on_weekend(self):
        weekend_date = date(2016,5,7)
        self.tr.updated_at = weekend_date
        dates = Session.make_dates(self.tr)
        expected_end_date = date(2016,5,30)
        expected_start_date = date(2016,5,9)
        self.assertEqual(expected_end_date, dates[-1])
        self.assertEqual(expected_start_date, dates[0])

    def test_that_make_dates_makes_dates(self):
        amb = User.objects.create(username="foo")
        diff = timezone.now() + timedelta(weeks=-5)
        semester = Semester.objects.create(start_date=diff,
               end_date=timezone.now())
        course = Course.objects.create(name="MAC2311", team_leader=amb)
        av = Availability.objects.create(ambassador=amb,
                                        start_time='11:00:00',
                                        end_time='12:00:00',
                                        semester=semester)
        request = TutoringRequest.objects.create(submitted_by=amb,
                availability = av,
                course=course,
                updated_at = timezone.now()+timedelta(weeks=-2)
                )
        request = TutoringRequest.objects.get(pk=request.pk)
        dates = Session.make_dates(request)
        self.assertTrue(dates)

class IndividualSessionModelTest(TestCase):
    def setUp(self):
        self.amb = User.objects.create(username="foo")
        diff = timezone.now() + timedelta(weeks=-5)
        semester = Semester.objects.create(start_date=diff,
               end_date=timezone.now())
        course = Course.objects.create(name="MAC2311", team_leader=self.amb)
        self.av = Availability.objects.create(ambassador=self.amb,
                                        start_time='11:00:00',
                                        end_time='12:00:00',
                                        day=timezone.now().isoweekday(),
                                        semester=semester)
        self.request = TutoringRequest.objects.create(submitted_by=self.amb,
                availability = self.av,
                course=course,
                updated_at = timezone.now()+timedelta(weeks=-3)
                )

    def test_that_sessions_get_made(self):
        request = TutoringRequest.objects.get()
        dates = Session.make_dates(request)
        session = Session.objects.create(
                ambassador = self.amb,
                start_time = self.av.start_time,
                end_time = self.av.end_time,
                day_of_week = self.av.day,
                availability = request.availability,
                tutee = request.submitted_by,
                course = request.course,
                end_date = dates[-1],
                start_date = dates[0]
                )
        IndividualSession.make_from_dates(session, dates)
        sessions = IndividualSession.objects.all()
        self.assertTrue(sessions)
        self.assertTrue(sessions.count() > 1)

    def test_that_from_dates_returns_a_list_of_sessions(self):
        request = TutoringRequest.objects.get()
        dates = Session.make_dates(request)
        session = Session.objects.create(
                ambassador = self.amb,
                start_time = self.av.start_time,
                end_time = self.av.end_time,
                day_of_week = self.av.day,
                availability = request.availability,
                tutee = request.submitted_by,
                course = request.course,
                end_date = dates[-1],
                start_date = dates[0]
                )
        s = IndividualSession.make_from_dates(session, dates)
        self.assertTrue(s)
        self.assertEqual(len(s), 2)

    def test_that_get_dates_returns_accurate_dates(self):
        request = TutoringRequest.objects.get()
        dates = Session.make_dates(request)
        session = Session.objects.create(
                ambassador = self.amb,
                start_time = self.av.start_time,
                end_time = self.av.end_time,
                day_of_week = self.av.day,
                availability = request.availability,
                tutee = request.submitted_by,
                course = request.course,
                end_date = dates[-1],
                start_date = dates[0]
                )
        get_dates = session.get_dates()
        self.assertEqual(dates,get_dates)

class IndividualSessionMethodsTest(SessionSetUp):
    def test_that_swap_sessions_actually_swaps_sessions(self):
        request = TutoringRequest.objects.get()
        dates = Session.make_dates(request)
        old_session = Session.objects.create(
                ambassador = self.amb,
                start_time = self.av.start_time,
                end_time = self.av.end_time,
                day_of_week = self.av.day,
                availability = request.availability,
                tutee = request.submitted_by,
                course = request.course,
                end_date = dates[-1],
                start_date = dates[0]
                )
        individual_sessions = IndividualSession.make_from_dates(
                old_session, dates)
        availability = request.availability
        availability.pk = None
        availability.save()
        new_session = Session.objects.create(
                ambassador = self.amb,
                start_time = self.av.start_time,
                end_time = self.av.end_time,
                day_of_week = self.av.day,
                availability = availability,
                tutee = request.submitted_by,
                course = request.course,
                end_date = dates[-1],
                start_date = dates[1]
                )
        IndividualSession.swap_sessions_with_session(
                new_session, old_session)
        sessions = IndividualSession.objects.filter(session=new_session)
        self.assertTrue(sessions)
        self.assertEqual(sessions.count(), len(individual_sessions) - 1)

    def test_that_swap_with_form_swaps_sessions(self):
        amb2 = User.objects.create(username='amb2')
        request = TutoringRequest.objects.get()
        dates = Session.make_dates(request)
        old_session = Session.objects.create(
                ambassador = self.amb,
                start_time = self.av.start_time,
                end_time = self.av.end_time,
                day_of_week = self.av.day,
                availability = request.availability,
                tutee = request.submitted_by,
                course = request.course,
                end_date = dates[-1],
                start_date = dates[0]
                )
        individual_sessions = IndividualSession.make_from_dates(
                old_session, dates)
        data = {
                'ambassador' : amb2.pk,
                'start_date' : dates[1],
                }
        form = TutoringSessionUpdateForm(
                instance=old_session,
                data=data)
        self.assertTrue(form.is_valid())
        new_session = Session.duplicate_for_swap(form)
        self.assertNotEqual(new_session.pk, old_session.pk)
        IndividualSession.swap_sessions_with_form(
                new_session, form)
        sessions = IndividualSession.objects.filter(session=new_session)
        self.assertTrue(sessions)
        self.assertEqual(sessions.count(), len(individual_sessions) - 1)
