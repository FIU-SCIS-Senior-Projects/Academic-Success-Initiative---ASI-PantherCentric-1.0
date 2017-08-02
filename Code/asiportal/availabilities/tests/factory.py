import factory
from datetime import time
from availabilities.models import Availability
from asiapp.tests import base_factory as userfactory
from semesters.tests import factory as semesterfactory
class AvailabilityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Availability
    start_time = time(11,0,0)
    end_time = time(12,0,0)
    day = 1

    # foreign keys
    ambassador = factory.SubFactory(userfactory.AmbassadorUserFactory)
    semester = factory.SubFactory(semesterfactory.SemesterFactory)
