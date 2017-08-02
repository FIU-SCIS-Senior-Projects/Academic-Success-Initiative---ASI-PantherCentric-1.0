from datetime import timedelta
from django.db import models
from django.db.models import Q
import django.utils.timezone
from django.utils import timezone
from django.utils.text import slugify

class SemesterQuerySet(models.query.QuerySet):
    def current(self):
        now = timezone.now().date()
        if self.all():
            qs = self.order_by('-end_date')
            if qs[0].term in ['SC','SB','SA']:
                return self.filter(
                        Q(term='SA') | Q(term='SB') | Q(term='SC'),
                        year=now.year)
            else:
                return self.filter(start_date__lte = now,
                                   end_date__gte = now,
                                   year = now.year)
        else:
            return self.all()

class SemesterManager(models.Manager):
    def get_queryset(self):
        return SemesterQuerySet(self.model, using=self._db)
    def current(self):
        return self.get_queryset().current()

class Semester(models.Model):
    TERMS = (
            ('FA', 'Fall'),
            ('SA', 'Summer A'),
            ('SB', 'Summer B'),
            ('SC', 'Summer C'),
            ('SP', 'Spring'),
            )
    term = models.CharField(max_length=2,
                            choices=TERMS, 
                            default='FA'
                            )
    start_date = models.DateField(default=django.utils.timezone.now)
    end_date = models.DateField(default=django.utils.timezone.now)
    year = models.IntegerField(default=django.utils.timezone.now().year)
    slug = models.SlugField(max_length=20, blank=True)
    objects = SemesterManager()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.__str__())
        super(Semester, self).save(*args,**kwargs)

    def __str__(self):
        return '%s %s' % (self.get_term_display(), self.year)

    def is_summer(self):
        if self.term in ['SA', 'SB', 'SC']:
            return True
        else:
            return False
