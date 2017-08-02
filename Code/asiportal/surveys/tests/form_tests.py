from django.test import TestCase
from asiapp.tests.base_factory import UserFactory
from availabilities.tests.factory import AvailabilityFactory
from courses.models import Course
from semesters.tests.factory import SemesterFactory
from surveys.models import AmbassadorSurvey
from tutoring_sessions.tests.factory import SessionFactory
from surveys.forms import AmbassadorSurveyForm
from surveys.forms import TuteeSurveyForm

class AmbassadorFormsTest(TestCase):

    def setUp(self):
        self.amb = AmbassadorUserFactory()
        self.course = Course.objects.create(name='MAC2311')
        self.sem = SemesterFactory()
        self.ava = AvailabilityFactory(
                    ambassador=self.amb,
                    semester=self.sem,
                    )
        self.tut = TuteeUserFactory()
        self.ses = SessionFactory(
                    availability = self.ava,
                    tutee=self.tut,
                    course=self.course,
                    )
        self.surv = AmbassadorSurvey.objects.create(
                    session = self.ses,
                    rating_1 = 5,
                    rating_2 = 5,
                    rating_3 = 5,
                    )

    def test_form_is_valid(self):
        form_data =
        form = AmbassadorSurveyForm(data=form_data)
        self.assertTrue()


class TuteeFormsTest(TestCase):

    def setUp(self):
        self.amb = AmbassadorUserFactory()
        self.course = Course.objects.create(name='MAC2311')
        self.sem = SemesterFactory()
        self.ava = AvailabilityFactory(
                    ambassador=self.amb,
                    semester=self.sem,
                    )
        self.tut = TuteeUserFactory()
        self.ses = SessionFactory(
                    availability = self.ava,
                    tutee=self.tut,
                    course=self.course,
                    )
        self.surv = TuteeSurvey.objects.create(
                    session = self.ses,
                    rating_1 = 5,
                    rating_2 = 5,
                    rating_3 = 5,
                    rating_4 = 5,
                    rating_5 = 5,
                    rating_6 = 5,
                    rating_7 = 5,
                    )

