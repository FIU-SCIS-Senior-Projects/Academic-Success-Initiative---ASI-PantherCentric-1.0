import factory
from courses.models import Course
from asiapp.tests.base_factory import AmbassadorUserFactory

class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Course

    name = "CDA 3103"
    team_leader = factory.SubFactory(AmbassadorUserFactory)
