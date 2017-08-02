from datetime import datetime, date, timedelta
import pytz
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from rquests.models import TutoringRequest
from rquests.services.session_maker import make_dates
from rquests.services.ticket_updates import update_other_times
from availabilities.models import Availability
from courses.models import Course
from semesters.models import Semester
from tutoring_sessions.models import Session

class TicketUpdaterTest(TestCase):
    def test_ticket_updates_own_time(self):
        amb = User.objects.create(username='amb')
        semester = Semester.objects.create(start_date=date(2016,5,5),
                                           end_date=date(2016,6,6))
        av = Availability.objects.create(ambassador=amb,
                                         start_time='11:00:00',
                                         end_time='12:00:00',
                                         semester=semester,)
        update_other_times(av)
        self.assertFalse(av.room_available)

    def test_ticket_updates_other_times(self):
        amb = User.objects.create(username='amb')
        amb2 = User.objects.create(username='amb2')
        semester = Semester.objects.create(start_date=date(2016,5,5),
                                           end_date=date(2016,6,6))

        av = Availability.objects.create(ambassador=amb,
                                         start_time='11:00:00',
                                         end_time='12:00:00',
                                         semester=semester,)

        av2 = Availability.objects.create(ambassador=amb2,
                                         start_time='11:00:00',
                                         end_time='12:00:00',
                                         semester=semester,)
        update_other_times(av)
        no_rooms = Availability.objects.filter(room_available=False)
        self.assertIn(av, no_rooms)
        self.assertIn(av2, no_rooms)
