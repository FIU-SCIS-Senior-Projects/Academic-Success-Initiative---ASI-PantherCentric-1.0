import factory
from django.utils import timezone
from surveys import models
from tutoring_sessions.tests import factory as sesfactory

class AmbassadorSurveyFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.AmbassadorSurvey
    rating_1 = 5
    rating_2 = 5
    rating_3 = 5
    comments = "This guy is cool I guess"
    session_canceled = False
    tutee_absent = False
    canceled_session_reason = ""
    submitted_at = timezone.now()
    submitted = False

    #foreign key
    individual_session = factory.SubFactory(sesfactory.IndividualSessionFactory)

class TuteeSurveyFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.TuteeSurvey
    rating_1 = 5
    rating_2 = 5
    rating_3 = 5
    rating_4 = 5
    rating_5 = 5
    rating_6 = 5
    rating_7 = 5
    comments = "He's a cool dude"
    submitted_at = timezone.now()
    submitted = False

    #foreign key
    individual_session = factory.SubFactory(sesfactory.IndividualSessionFactory)

