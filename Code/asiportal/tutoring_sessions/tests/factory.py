import factory
from datetime import date, timedelta
from django.utils import timezone
from tutoring_sessions.models import Session, IndividualSession
from availabilities.tests import factory as availfactory
from asiapp.tests import base_factory as userfactory
from courses.tests import factory as coursefactory

class SessionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Session

    start_date = timezone.now()
    end_date = timezone.now() + timedelta(weeks=4)

    # foreign keys
    availability = factory.SubFactory(availfactory.AvailabilityFactory)
    tutee = factory.SubFactory(userfactory.TuteeUserFactory)
    course = factory.SubFactory(coursefactory.CourseFactory)
    ambassador = factory.SubFactory(userfactory.TuteeUserFactory)
    start_time = timezone.now()
    end_time = timezone.now()

class IndividualSessionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = IndividualSession

    session_date = timezone.now()

    # foreign key
    session = factory.SubFactory(SessionFactory)
