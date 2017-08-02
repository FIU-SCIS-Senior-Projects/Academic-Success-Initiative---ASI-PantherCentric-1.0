# Django
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Local Django
from tutoring_sessions.models import Session
from rquests.models import TutoringRequest


class TimeRestrictionQuerySet(models.query.QuerySet):
    def overtime(self):
        qs = self.prefetch_related('user').all()
        over = [q.user.pk for q in qs if q.is_over_time()]
        return User.objects.filter(pk__in = over)


class TimeRestrictionManager(models.Manager):
    def get_queryset(self):
        return TimeRestrictionQuerySet(self.model, using=self._db)
    def overtime(self):
        return self.get_queryset().overtime()

class TimeRestriction(models.Model):
    max_time = models.PositiveIntegerField(default=20)
    user = models.ForeignKey(User, related_name='restrictions')
    objects = TimeRestrictionManager()

    def is_over_time(self):
        current_time = Session.objects.filter(
                availability__ambassador__pk = self.user.pk,
                end_date__gte = timezone.now()
                ).count()
        maybe_time = TutoringRequest.objects.filter(
                availability__ambassador__pk = self.user.pk,
                status = 'A',
                ).count()
        if ( current_time + maybe_time ) >= self.max_time:
            return True
        else:
            return False

