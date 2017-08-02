# standard library
import datetime

# Django
from django.db import models
from django.utils.crypto import get_random_string
from django.core.urlresolvers import reverse

# local Django
from tutoring_sessions.models import Session, IndividualSession

class Survey(models.Model):
    rating_1 = models.IntegerField(default=3)
    rating_2 = models.IntegerField(default=3)
    rating_3 = models.IntegerField(default=3)
    individual_session = models.ForeignKey(
              IndividualSession,
              on_delete=models.CASCADE,
              related_name="%(app_label)s_%(class)s_related")
    slug = models.SlugField(
            unique=True,
            default=get_random_string,
            max_length=32,
            )
    submitted_at = models.DateTimeField(auto_now=True)
    session_canceled = models.BooleanField(default=False)
    tutee_absent = models.BooleanField(default=False)
    comments = models.CharField(max_length=140)
    submitted = models.BooleanField(default=False)

    def average_rating(self):
        """
        Returns the average rating given for an Tutee given by an Ambassador
        """
        return ( self.rating_1 + self.rating_2 + self.rating_3) / 3

    @classmethod
    def create_surveys_from_individual_sessions(cls, sessions):
        """
        Takes a list of Individual Sessions, creates an Ambassador Survey or Tutee Survey for each Individual Session in the list and saves the surveys.
        """
        return [cls.objects.create(individual_session=session) for session in sessions]

    class Meta:
        abstract=True

class AmbassadorSurvey(Survey):
    canceled_session_reason = models.CharField(max_length=140, blank=True)

    def get_absolute_url(self):
        return reverse('surveys:ambassador_survey', kwargs={'slug': self.slug })

    def get_date(self):
        """
        Returns date of an Individual Session
        """
        return self.individual_session.session_date.strftime('%A')

    def get_tutee(self):
        """
        Returns the name of a Tutee
        """
        return self.individual_session.session.tutee.get_full_name()

    def __str__(self):
        return '{} for {}'.format(self.__class__.__name__, self.individual_session.session.availability.ambassador.get_full_name())

class TuteeSurvey(Survey):
    rating_4 = models.IntegerField(default=3)
    rating_5 = models.IntegerField(default=3)
    rating_6 = models.IntegerField(default=3)
    rating_7 = models.IntegerField(default=3)
    wearing_shirt = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('surveys:tutee_survey', kwargs={'slug': self.slug })

    def average_rating(self):
        """
        Returns the average rating given for an Ambassador given by a Tutee
        """
        return ( self.rating_1 + self.rating_2 + self.rating_3 + self.rating_4 + self.rating_5 + self.rating_6 + self.rating_7) / 7

    def __str__(self):
        return '{} for {}'.format(self.__class__.__name__, self.individual_session.session.tutee.get_full_name())
