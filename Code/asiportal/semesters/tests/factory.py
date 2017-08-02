import factory
from django.utils import timezone
from datetime import timedelta
from semesters.models import Semester

class SemesterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Semester
    start_date = timezone.now()
    end_date = timezone.now() + timedelta(weeks=4)
