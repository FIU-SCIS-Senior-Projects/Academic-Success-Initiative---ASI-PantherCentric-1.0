#from django.test import TestCase
from unittest import TestCase
from unittest.mock import Mock
from surveys.models import AmbassadorSurvey, TuteeSurvey
from admindashboard.services.averager import (
        overall_averages,
        calculate_total_absences)

class TestOverallAmbassadorAverageService(TestCase):

    def test_overall_average_calculates_correctly_with_one(self):
        survey = AmbassadorSurvey()
        survey.rating_1 = 5
        survey.rating_2 = 5
        survey.rating_3 = 5
        surveys = [survey]
        average = overall_averages(surveys, **{
            "rating_1" : "rating_1",
            "rating_2" : "rating_2",
            "rating_3" : "rating_3",
            })
        self.assertEqual(average['rating_1'], 5.0)
        self.assertEqual(average['rating_2'], 5.0)
        self.assertEqual(average['rating_3'], 5.0)

    def test_overall_average_calculates_correctly_with_many(self):
        survey_1 = AmbassadorSurvey()
        survey_2 = AmbassadorSurvey()
        survey_1.rating_1 = 5
        survey_1.rating_2 = 5
        survey_1.rating_3 = 5
        survey_2.rating_1 = 3
        survey_2.rating_2 = 3
        survey_2.rating_3 = 3
        surveys = [survey_1, survey_2]
        average = overall_averages(surveys, **{
            "rating_1" : "rating_1",
            "rating_2" : "rating_2",
            "rating_3" : "rating_3",
            })
        self.assertEqual(average['rating_1'], 4.0)
        self.assertEqual(average['rating_2'], 4.0)
        self.assertEqual(average['rating_3'], 4.0)

    def test_overall_average_doesnt_calculate_empty_surveys(self):
        surveys = []
        average = overall_averages(surveys, **{
            "rating_1" : "rating_1",
            "rating_2" : "rating_2",
            "rating_3" : "rating_3",
            })
        self.assertEqual(average['rating_1'],0)
        self.assertTrue(average['errors'])
        self.assertEqual(average['rating_2'],0)
        self.assertEqual(average['rating_3'],0)
        self.assertEqual(average['message'], "No surveys to average.")

class TestOverallTuteeAverageService(TestCase):

    def test_overall_average_calculates_correctly_with_one(self):
        survey = TuteeSurvey()
        survey.rating_1  = 5
        survey.rating_2  = 5
        survey.rating_3  = 5
        survey.rating_4  = 5
        survey.rating_5  = 5
        survey.rating_6  = 5
        survey.rating_7  = 5

        average = overall_averages([survey], 
                **{
                    'rating_1' : 'rating_1',
                    'rating_2' : 'rating_2',
                    'rating_3' : 'rating_3',
                    'rating_4' : 'rating_4',
                    'rating_5' : 'rating_5',
                    'rating_6' : 'rating_6',
                    'rating_7' : 'rating_7',
                    })
        self.assertEqual(average['rating_1'], 5.0)
        self.assertEqual(average['rating_2'], 5.0)
        self.assertEqual(average['rating_3'], 5.0)
        self.assertEqual(average['rating_4'], 5.0)
        self.assertEqual(average['rating_5'], 5.0)
        self.assertEqual(average['rating_6'], 5.0)
        self.assertEqual(average['rating_7'], 5.0)

    def test_overall_average_calculates_correctly_with_many(self):
        survey1 = TuteeSurvey()
        survey1.rating_1  = 5
        survey1.rating_2  = 5
        survey1.rating_3  = 5
        survey1.rating_4  = 5
        survey1.rating_5  = 5
        survey1.rating_6  = 5
        survey1.rating_7  = 5

        survey2 = TuteeSurvey()
        survey2.rating_1  = 3
        survey2.rating_2  = 3
        survey2.rating_3  = 3
        survey2.rating_4  = 3
        survey2.rating_5  = 3
        survey2.rating_6  = 3
        survey2.rating_7  = 3


        average = overall_averages([survey1, survey2], 
                **{
                    'rating_1' : 'rating_1',
                    'rating_2' : 'rating_2',
                    'rating_3' : 'rating_3',
                    'rating_4' : 'rating_4',
                    'rating_5' : 'rating_5',
                    'rating_6' : 'rating_6',
                    'rating_7' : 'rating_7',
                    })
        self.assertEqual(average['rating_1'], 4.0)
        self.assertEqual(average['rating_2'], 4.0)
        self.assertEqual(average['rating_3'], 4.0)
        self.assertEqual(average['rating_4'], 4.0)
        self.assertEqual(average['rating_5'], 4.0)
        self.assertEqual(average['rating_6'], 4.0)
        self.assertEqual(average['rating_7'], 4.0)

    def test_overall_average_doesnt_calculate_zero(self):
        average = overall_averages([],  **{
                    'rating_1' : 'rating_1',
                    'rating_2' : 'rating_2',
                    'rating_3' : 'rating_3',
                    'rating_4' : 'rating_4',
                    'rating_5' : 'rating_5',
                    'rating_6' : 'rating_6',
                    'rating_7' : 'rating_7',
                    })
        self.assertTrue(average['errors'])
        self.assertEqual(average['rating_1'], 0)
        self.assertEqual(average['rating_2'], 0)
        self.assertEqual(average['rating_3'], 0)
        self.assertEqual(average['rating_4'], 0)
        self.assertEqual(average['rating_6'], 0)
        self.assertEqual(average['rating_7'], 0)
        self.assertEqual(average['message'], "No surveys to average.")

class AbsenceCounterTest(TestCase):
    def test_that_absences_get_counted_correctly(self):
        # absences are recoreded in both the ambassador and tutee survey
        # so we can use either to extrapolate the information
        survey = TuteeSurvey()
        survey.tutee_absent= True
        total_absences = calculate_total_absences([survey])
        self.assertEqual(total_absences['absences'], 1)
        self.assertEqual(total_absences['total_sessions'], 1)

    def test_that_absences_dont_count_if_session_canceled(self):
        survey = TuteeSurvey()
        survey.tutee_absent = True
        survey.session_canceled = True
        total_absences = calculate_total_absences([survey])
        self.assertEqual(total_absences['absences'], 0)
        self.assertEqual(total_absences['total_sessions'], 0)

    def test_that_absences_dont_count_if_session_canceled_and_counts(self):
        survey = TuteeSurvey()
        survey.tutee_absent = True
        survey.session_canceled = True
        survey2 = TuteeSurvey()
        survey2.tutee_absent = True
        survey2.session_canceled = False
        total_absences = calculate_total_absences([survey, survey2])
        self.assertEqual(total_absences['absences'], 1)
        self.assertEqual(total_absences['total_sessions'], 1)

    def test_that_when_student_is_present_no_absences_recorded(self):
        survey = TuteeSurvey()
        survey.tutee_absent = False
        survey.session_canceled = False
        total_absences = calculate_total_absences([survey])
        self.assertEqual(total_absences['absences'], 0)
        self.assertEqual(total_absences['total_sessions'], 1)

    def test_that_when_no_surveys_numbers_make_sense(self):
        total_absences = calculate_total_absences([])
        self.assertEqual(total_absences['absences'], 0)
        self.assertEqual(total_absences['total_sessions'], 0)
