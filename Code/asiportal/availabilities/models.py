from datetime import time
from itertools import takewhile
from django.contrib.auth.models import User
from django.db import models, IntegrityError
from django.utils import timezone
from semesters.models import Semester

class Availability(models.Model):
    # class Meta:
    #     unique_together = (('ambassador', 'semester'), ('start_time', 'day'))
    DAYS = (
            (1,'Monday'),
            (2,'Tuesday'),
            (3,'Wednesday'),
            (4,'Thursday'),
            (5,'Friday'),
            )

    ambassador = models.ForeignKey(
                 User,
                 related_name = 'availabilities',
                 limit_choices_to={'is_staff': True},
                 )

    semester = models.ForeignKey(
                Semester,
                related_name='availabilities_for_semester'
                )

    start_time = models.TimeField()
    end_time = models.TimeField()
    day = models.IntegerField(choices=DAYS, default=1)
    room_available = models.BooleanField(default=True)
    is_scheduled = models.BooleanField(default=False)

    def __str__(self):
        return "%s on %s from %s - %s" % (
                self.ambassador.get_full_name(),
                self.get_day_display(),
                self.start_time.strftime('%-I:%M %p'),
                self.end_time.strftime('%-I:%M %p'),
                )

    def exists(self):
        if Availability.objects.filter(
                ambassador = self.ambassador,
                semester = self.semester,
                start_time = self.start_time,
                day=self.day):
            return True
        else:
            return False

    def create(self):
        if self.exists():
            raise IntegrityError
        else:
            self.save()

    @staticmethod
    def create_from_form(ambassador, form):
        a = Availability.set_up(ambassador, form)
        a.create()
        if a.semester.term == 'SC':
            a2 = Availability.set_up(ambassador, form)
            a2.semester = Semester.objects.get(term='SA',
                    year=timezone.now().year)
            a2.create()
            a3 = Availability.set_up(ambassador, form)
            a3.semester = Semester.objects.get(term='SB',
                    year=timezone.now().year)
            a3.create()

    @staticmethod
    def create_with_times(ambassador, form):
        for t in takewhile(lambda t: t != form._times[-1], form._times):
            a = Availability.set_up(ambassador, form, start=t)
            a.create()

    @staticmethod
    def set_up(ambassador, form, **kwargs):
        base = form.save(commit=False)
        ava = Availability()
        ava.ambassador = ambassador
        ava.semester = base.semester
        ava.day = base.day
        if kwargs:
            start = kwargs.get('start')
            ava.start_time = start
            ava.end_time = time(start.hour + 1, 0 ,0)
        else:
            ava.start_time = base.start_time
            ava.end_time = base.end_time
        return ava

    def find_related_summer(self):
        if self.semester.term == 'SC':
            pots = Availability.objects.filter(
                    ambassador=self.ambassador,
                    day=self.day,
                    start_time=self.start_time,
                    end_time=self.end_time,
                    semester__term__in = ['SA', 'SB'],
                    semester__year=self.semester.year
                    )
            return pots
        elif self.semester.term in ['SB', 'SA']:
            pots = Availability.objects.filter(
                    ambassador=self.ambassador,
                    day=self.day,
                    start_time=self.start_time,
                    end_time=self.end_time,
                    semester__term = 'SC',
                    semester__year=self.semester.year
                    )
            return pots
        else:
            return []
