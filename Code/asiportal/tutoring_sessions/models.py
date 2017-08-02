from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import User
from availabilities.models import Availability
from courses.models import Course

ROOMS = (
        ('101A','101A'),
         ('101B','101B'),
         ('101C', '101C'),
         ('101D', '101D'),
         )

DAYS = (
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        )

class Session(models.Model):
    ambassador = models.ForeignKey(User,
            related_name = 'ambassador_sessions'
            )

    start_time = models.TimeField()

    end_time = models.TimeField()

    day_of_week = models.IntegerField(choices=DAYS,
            default=1)

    availability = models.ForeignKey(
                    Availability,
                    related_name='session',
                    )

    tutee = models.ForeignKey(
                    User,
                    related_name = 'sessions'
                    )
    course = models.ForeignKey(
                    Course,
                    related_name = 'course_sessions',
                    )
    room_number = models.CharField(choices=ROOMS,
                                    max_length=4,
                                    default='101A')
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return "%s with %s for %s" % (
                self.ambassador.get_full_name(),
                self.tutee.get_full_name(),
                self.course,
                )

    @staticmethod
    def make_dates(request):
        availability = request.availability
        updated_at = request.updated_at
        if isinstance(updated_at, datetime):
            updated_at = updated_at.date()
        semester = availability.semester
        start_diff =  availability.day - updated_at.isoweekday()
        end_diff = availability.day - semester.end_date.isoweekday()
        # the last session should take place on the week before
        # the last week of the semester on the correct availability day

        if updated_at < semester.start_date:
            start_date = semester.start_date + timedelta(weeks=1,days=start_diff)
            end_date = semester.end_date - timedelta(weeks=1,days=end_diff)
        else:
            # if we land on sunday and the next day is monday then always schedule 1 week ahead
            if (updated_at.isoweekday() == 7 and start_diff == -6):
                start_date = updated_at + timedelta(weeks=1, days=1)
                end_date = semester.end_date - timedelta(weeks=1,days=end_diff)
            elif start_diff >= 2:
                start_date = updated_at + timedelta(days=start_diff)
                end_date = semester.end_date - timedelta(weeks=1,days=end_diff)
            else:
                start_date = updated_at + timedelta(weeks=1, days=start_diff)
                end_date = semester.end_date - timedelta(weeks=1,days=end_diff)
        days = (end_date - start_date).days + 1
        dates = [date for date in (start_date + timedelta(days=n) for n in range(days)) if date.isoweekday() == availability.day]
        return dates

    def get_dates(self):
        days = (self.end_date - self.start_date).days + 1
        semester = self.availability.semester
        dates = [date for date in (self.start_date + timedelta(days=n) for n in range(days)) if date.isoweekday() == self.availability.day]
        return dates

    @staticmethod
    def duplicate_for_swap(form):
        old_session = form.save(commit=False)
        availability = old_session.availability
        avas = Availability.objects.filter(
                start_time = availability.start_time,
                end_time = availability.end_time,
                day = availability.day,
                semester = availability.semester,
                ambassador = form.cleaned_data['ambassador']
                )
        if avas:
            availability = avas[0]
        else:
            availability.pk = None
            availability.ambassador = form.cleaned_data['ambassador']
            availability.save()
        new_session = Session()
        new_session.availability = availability
        new_session.ambassador = availability.ambassador
        new_session.start_time = availability.start_time
        new_session.end_time = availability.end_time
        new_session.day_of_week = availability.day
        new_session.course = old_session.course
        new_session.tutee = old_session.tutee
        new_session.start_date = form.cleaned_data['start_date']
        new_session.end_date = old_session.end_date
        new_session.room_number = old_session.room_number
        new_session.save()
        return new_session

    def create_from_form(self, form):
        request = form.save()
        dates = self.make_dates(request)
        session = Session()
        session.room_number = form.cleaned_data['room_number']
        session.ambassador = request.availability.ambassador
        session.start_time = request.availability.start_time
        session.end_time = request.availability.end_time
        session.day_of_week = request.availability.day
        session.start_date = dates[0]
        session.end_date = dates[-1]
        session.tutee = request.submitted_by
        session.course = request.course
        session.availability = request.availability
        session.availability.is_scheduled = True
        session.availability.save()
        session.save()
        sessions = IndividualSession.make_from_dates(session, dates)
        return sessions

class IndividualSession(models.Model):
    session = models.ForeignKey(
        Session,
        related_name='individual_sessions')
    session_date = models.DateField()

    @staticmethod
    def make_from_dates(session, dates):
        sessions = list()
        for date in dates:
            individual_session = IndividualSession()
            individual_session.session = session
            individual_session.session_date = date
            individual_session.save()
            sessions.append(individual_session)
        return sessions

    @staticmethod
    def swap_sessions_with_form(new_session, form):
        old_session = form.save(commit=False)
        sessions = IndividualSession.objects.filter(
                session_date__gte=form.cleaned_data['start_date'],
                session = old_session,
                )
        for s in sessions:
            s.session = new_session
            s.save()

    @staticmethod
    def swap_sessions_with_session(new_session, old_session):
        sessions = IndividualSession.objects.filter(
                session_date__gte = new_session.start_date,
                session = old_session,
                )
        for s in sessions:
            s.session = new_session
            s.save()

    @staticmethod
    def remove_after_date(session, date):
        inds = IndividualSession.objects.filter(
                session = session,
                session_date__gte = date,)
        for i in inds:
            i.delete()

    def __str__(self):
        return '{} on {:%b, %d %Y}'.format(self.session, self.session_date)
