from django.test import TestCase
from surveys.models import AmbassadorSurvey, TuteeSurvey
from tutoring_sessions.tests.factory import IndividualSessionFactory

class AmbassadorSurveyTest(TestCase):

    def setUp(self):
        self.inses = IndividualSessionFactory()

    def test_survey_is_made(self):
        AmbassadorSurvey.create_surveys_from_individual_sessions([self.inses])
        self.assertTrue(AmbassadorSurvey.objects.all())

    def test_surveys_are_made(self):
        self.inses2 = IndividualSessionFactory()
        sessions = [self.inses, self.inses2]
        AmbassadorSurvey.create_surveys_from_individual_sessions(sessions)
        surveys = AmbassadorSurvey.objects.all()
        self.assertNotEqual(surveys[0].individual_session, surveys[1].individual_session)

class TuteeSurveyTest(TestCase):

    def setUp(self):
        self.inses = IndividualSessionFactory()

    def test_survey_is_made(self):
        TuteeSurvey.create_surveys_from_individual_sessions([self.inses])
        self.assertTrue(TuteeSurvey.objects.all())
