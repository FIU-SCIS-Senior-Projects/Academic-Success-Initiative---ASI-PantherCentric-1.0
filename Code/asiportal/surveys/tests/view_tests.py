# Django
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.db.models import Q

# Django Testing
from django.test import(
    TestCase,
    RequestFactory,
    TransactionTestCase,
)

# standard library
from datetime import timedelta

# factories
from surveys.tests.factory import AmbassadorSurveyFactory
from surveys.tests.factory import TuteeSurveyFactory
from asiapp.tests.base_factory import AmbassadorUserFactory, TuteeUserFactory
from semesters.tests.factory import SemesterFactory
from courses.tests.factory import CourseFactory

# local Django
from surveys.models import AmbassadorSurvey, TuteeSurvey
from tutoring_sessions.models import IndividualSession, Session
from availabilities.models import Availability
from tutoring_sessions.tests.factory import IndividualSessionFactory

# Other
from freezegun import freeze_time

# @alan
# couldn't load this view, maybe forgot to delete?
from surveys.views import (#GeneralSurveyView,
                    AmbassadorSurveyView,
                    AmbassadorListSurveysView,
                    TuteeSurveyView,
                    TuteeListSurveysView,
                    TuteeListCourseSurveysView,
                    SurveyStatusListView,
                    )
#get and post

''' Testing Ambassadors Survey View
    --------------------------------
    What to test:
        1) Can surveys be rendered correctly
        2) Are the right surveys returned
        3) Is the correct session attatched to a survey
        4) Can the survey be submitted '''

def setup_view(view, request, *args, **kwargs):
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view

class AmbassadorSurveyViewTest(TestCase):
    #setup needs the list of surveys that have already been created
        #ambassador, session, tutee for that survey, attributes of survey
    def setUp(self):
        self.factory = RequestFactory()
        self.surv = AmbassadorSurveyFactory()

    def test_ambassador_survey_can_be_submitted(self):
        data = {
                'rating_1': 5,
                'rating_2': 5,
                'rating_3': 2,
                'comments' : "This guy is cool I guess",
                'session_canceled' : False,
                'tutee_absent' : False,
                'canceled_session_reason' : "",
        }

        req =self.factory.post('/ambassador_survey', data)
        req.user = User.objects.create(username='alan')
        kwargs={'slug':self.surv.slug}
        response = AmbassadorSurveyView.as_view()(req, **kwargs)
        posted_data = AmbassadorSurvey.objects.get(pk=self.surv.pk)
        self.assertEqual(posted_data.rating_3, data['rating_3'])
        self.assertEqual(response.status_code, 302)

    #test tutee form fields overwritten when ambassador tutee_absent field is true
    def test_form_valid_tutee_absent_true(self):
        data = {
                'rating_1': 5,
                'rating_2': 5,
                'rating_3': 2,
                'comments' : "This guy is cool I guess",
                'session_canceled' : False,
                'tutee_absent' : True,
                'canceled_session_reason' : "",
        }

        self.tutsurv = TuteeSurveyFactory()
        tpk = self.tutsurv.pk
        self.tutsurv.individual_session = self.surv.individual_session
        self.tutsurv.save()

        req = self.factory.post('/ambassador_survey', data)
        req.user = self.surv.individual_session.session.availability.ambassador
        kwargs = {'slug':self.surv.slug}
        AmbassadorSurveyView.as_view()(req, **kwargs)

        retsurv = TuteeSurvey.objects.get(pk=tpk)

        self.assertTrue(retsurv.tutee_absent)
        self.assertTrue(retsurv.submitted)

    #test tutee form fields overwritten when ambassador session_canceled field is true
    def test_form_valid_session_canceled_true(self):
        data = {
                'rating_1': 5,
                'rating_2': 5,
                'rating_3': 2,
                'comments' : "This guy is cool I guess",
                'session_canceled' : True,
                'tutee_absent' : False,
                'canceled_session_reason' : "i hate tests",
        }

        self.tutsurv = TuteeSurveyFactory()
        tpk = self.tutsurv.pk
        self.tutsurv.individual_session = self.surv.individual_session
        self.tutsurv.save()

        req = self.factory.post('/ambassador_survey', data)
        req.user = self.surv.individual_session.session.availability.ambassador
        kwargs = {'slug':self.surv.slug}
        AmbassadorSurveyView.as_view()(req, **kwargs)

        retsurv = TuteeSurvey.objects.get(pk=tpk)

        self.assertTrue(retsurv.session_canceled)
        self.assertTrue(retsurv.submitted)

    def test_ambassador_survey_can_be_submitted_without_comment(self):
        data = {
                'rating_1': 5,
                'rating_2': 5,
                'rating_3': 2,
                'comments' : "",
                'session_canceled' : False,
                'tutee_absent' : False,
                'canceled_session_reason' : "",
        }

        req =self.factory.post('/ambassador_survey', data)
        req.user = User.objects.create(username='alan')
        kwargs={'slug':self.surv.slug}
        response = AmbassadorSurveyView.as_view()(req, **kwargs)

        self.assertEqual(response.status_code, 200)

class TuteeSurveyViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.surv = TuteeSurveyFactory()

    def test_tutee_can_submit_survey(self):
        data = {
                'rating_1': 5,
                'rating_2': 5,
                'rating_3': 2,
                'rating_4': 2,
                'rating_5': 2,
                'rating_6': 2,
                'rating_7': 2,
                'comments' : "This guy is cool I guess",
        }

        req =self.factory.post('/tutee_survey', data)
        req.user = User.objects.create(username='alan')
        kwargs={'slug':self.surv.slug}
        response = TuteeSurveyView.as_view()(req, **kwargs)
        posted_data = TuteeSurvey.objects.get(pk=self.surv.pk)
        self.assertEqual(posted_data.rating_3, data['rating_3'])
        self.assertEqual(response.status_code, 302)

    def test_tutee_can_submit_survey_without_comments(self):
        data = {
                'rating_1': 5,
                'rating_2': 5,
                'rating_3': 2,
                'rating_4': 2,
                'rating_5': 2,
                'rating_6': 2,
                'rating_7': 2,
                'comments' : "",
        }

        req =self.factory.post('/tutee_survey', data)
        req.user = User.objects.create(username='alan')
        kwargs={'slug':self.surv.slug}
        response = TuteeSurveyView.as_view()(req, **kwargs)
        posted_data = TuteeSurvey.objects.get(pk=self.surv.pk)
        self.assertEqual(response.status_code, 200)

class AmbassadorListSurveysViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.surv = AmbassadorSurveyFactory()

        #query set returned is the same as expected query set
    def test_get_queryset_with_session_that_have_not_happened(self):
        self.ses2 = IndividualSession.objects.create(
                session=self.surv.individual_session.session,
                session_date=(self.surv.individual_session.session_date + timedelta(weeks=1))
                )

        self.surv2 = AmbassadorSurvey.objects.create(
                rating_1= 5,
                rating_2= 5,
                rating_3= 2,
                comments = "This guy is cool I guess",
                session_canceled = False,
                tutee_absent = False,
                canceled_session_reason = "",
                submitted_at = timezone.now(),
                individual_session = self.ses2,
                submitted = False,
                )

        req = self.factory.get('/ambassador_survey_list')
        req.user = self.surv.individual_session.session.availability.ambassador
        response = AmbassadorListSurveysView.as_view()(req)
        queryset = response.context_data['object_list']

        self.assertIn(self.surv, queryset)
        self.assertNotIn(self.surv2, queryset)

    def test_get_queryset_different_users(self):
        self.ses2 = IndividualSessionFactory()
        self.ses2.session_date += timedelta(weeks=1)
        self.surv2 = AmbassadorSurvey.objects.create(
                rating_1= 5,
                rating_2= 5,
                rating_3= 2,
                comments = "This guy is cool I guess",
                session_canceled = False,
                tutee_absent = False,
                canceled_session_reason = "",
                individual_session = self.ses2,
                submitted = False,
                )

        req = self.factory.get('/ambassador_survey_list')
        req.user = self.surv.individual_session.session.availability.ambassador
        response = AmbassadorListSurveysView.as_view()(req)
        queryset = response.context_data['object_list']

        self.assertIn(self.surv, queryset)
        self.assertNotIn(self.surv2, queryset)

    def test_get_queryset_surveys_already_submitted(self):
        self.ses2 = IndividualSession.objects.create(
                session=self.surv.individual_session.session,
                session_date=(self.surv.individual_session.session_date - timedelta(weeks=1))
                )

        self.surv2 = AmbassadorSurvey.objects.create(
                rating_1= 5,
                rating_2= 5,
                rating_3= 2,
                comments = "This guy is cool I guess",
                session_canceled = False,
                tutee_absent = False,
                canceled_session_reason = "",
                submitted_at = self.ses2.session_date,
                individual_session = self.ses2,
                submitted = True,
                )

        req = self.factory.get('/ambassador_survey_list')
        req.user = self.surv.individual_session.session.availability.ambassador
        response = AmbassadorListSurveysView.as_view()(req)
        queryset = response.context_data['object_list']

        self.assertIn(self.surv, queryset)
        self.assertNotIn(self.surv2, queryset)



class TuteeSurveyViewTest(TestCase, TransactionTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.surv = TuteeSurveyFactory()

    def test_survey_can_be_submitted(self):
        data = {
                'rating_1': 5,
                'rating_2': 5,
                'rating_3': 2,
                'rating_4': 2,
                'rating_5': 2,
                'rating_6': 2,
                'rating_7': 2,
                'comments' : "This guy is cool I guess",
                'session_canceled' : False,
                'tutee_absent' : False,
                'submitted' : True
        }

        req = self.factory.post('/Tutee_survey', data)
        req.user = User.objects.create(username='alan')
        kwargs={'slug':self.surv.slug}
        response = TuteeSurveyView.as_view()(req, **kwargs)
        posted_data = TuteeSurvey.objects.get(pk=self.surv.pk)
        self.assertEqual(posted_data.rating_3, data['rating_3'])
        self.assertEqual(response.status_code, 302)

class TuteeListSurveysViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.surv = TuteeSurveyFactory()

        #query set returned is the same as expected query set
    def test_get_queryset_with_session_that_have_not_happened(self):
        self.ses2 = IndividualSession.objects.create(
                session=self.surv.individual_session.session,
                session_date=(self.surv.individual_session.session_date + timedelta(weeks=1))
                )

        self.surv2 = TuteeSurvey.objects.create(
                rating_1= 5,
                rating_2= 5,
                rating_3= 2,
                rating_4= 2,
                rating_5= 2,
                rating_6= 2,
                rating_7= 2,
                comments = "This guy is cool I guess",
                session_canceled = False,
                tutee_absent = False,
                submitted_at = timezone.now(),
                individual_session = self.ses2,
                submitted = False,
                )

        req = self.factory.get('/Tutee_survey_list')
        req.user = self.surv.individual_session.session.tutee
        response = TuteeListSurveysView.as_view()(req)
        queryset = response.context_data['object_list']

        self.assertIn(self.surv, queryset)
        self.assertNotIn(self.surv2, queryset)

    def test_get_queryset_different_users(self):
        self.ses2 = IndividualSessionFactory()
        self.ses2.session_date += timedelta(weeks=1)
        self.surv2 = TuteeSurvey.objects.create(
                rating_1= 5,
                rating_2= 5,
                rating_3= 2,
                rating_4= 2,
                rating_5= 2,
                rating_6= 2,
                rating_7= 2,
                comments = "This guy is cool I guess",
                session_canceled = False,
                tutee_absent = False,
                submitted_at = timezone.now(),
                individual_session = self.ses2,
                submitted = False,
                )

        req = self.factory.get('/Tutee_survey_list')
        req.user = self.surv.individual_session.session.tutee
        response = TuteeListSurveysView.as_view()(req)
        queryset = response.context_data['object_list']

        self.assertIn(self.surv, queryset)
        self.assertNotIn(self.surv2, queryset)

    def test_get_queryset_surveys_already_submitted(self):
        self.ses2 = IndividualSession.objects.create(
                session=self.surv.individual_session.session,
                session_date=(self.surv.individual_session.session_date - timedelta(weeks=1))
                )

        self.surv2 = TuteeSurvey.objects.create(
                rating_1= 5,
                rating_2= 5,
                rating_3= 2,
                rating_4= 2,
                rating_5= 2,
                rating_6= 2,
                rating_7= 2,
                comments = "This guy is cool I guess",
                session_canceled = False,
                tutee_absent = False,
                submitted_at = self.ses2.session_date,
                individual_session = self.ses2,
                submitted = True,
                )

        req = self.factory.get('/Tutee_survey_list')
        req.user = self.surv.individual_session.session.tutee
        response = TuteeListSurveysView.as_view()(req)
        queryset = response.context_data['object_list']

        self.assertIn(self.surv, queryset)
        self.assertNotIn(self.surv2, queryset)

class TuteeSurveyCourseListViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.surv = TuteeSurveyFactory()

        self.avail = Availability.objects.create(
                                ambassador=self.surv.individual_session.session.availability.ambassador,
                                semester=self.surv.individual_session.session.availability.semester,
                                start_time=timezone.now(),
                                end_time=timezone.now(),
                                )
        self.ses = Session.objects.create(
                            availability=self.avail,
                            ambassador = self.avail.ambassador,
                            start_time = self.avail.start_time,
                            end_time = self.avail.end_time,
                            day_of_week = self.avail.day,
                            tutee=self.surv.individual_session.session.tutee,
                            course=self.surv.individual_session.session.course,
                            start_date=timezone.now(),
                            end_date=timezone.now(),
                            )

        self.inses = IndividualSession.objects.create(
                session_date=timezone.now(),
                session=self.ses,
                )
        self.surv2 = TuteeSurvey.objects.create(individual_session=self.inses)

    def test_get_surveys_for_session(self):
        req = self.factory.get('/Tutee_survey_course_list')
        req.user = self.surv.individual_session.session.tutee
        kwargs={"session_pk":self.ses.pk}
        response  = TuteeListCourseSurveysView.as_view()(req, **kwargs)
        queryset = response.context_data['object_list']

        self.assertNotIn(self.surv, queryset)
        self.assertIn(self.surv2, queryset)

class SurveyStatusListViewTest(TestCase):
    '''
    Testing list view for tutee survey completion
        + set up will contain:
            Request factory
            Surveys
            Availability
            Sessions
            Individual Sessions

            Sessions (A), (B), (C)
                - (A): Belongs to session for query
                - (B): Belongs to some session (same ambassador) for query
                - (C): Does not belong to any sessions for ambassador
            List of surveys per session (A, B, C)

        + Tests:
            For each test assert the expected response for each list of surveys
                from session A, session B, session C

            1) Test that an incompleted survey is returned after session date
            2) Test that multiple incompleted surveys are returned after session date
            3) Test that an incompleted survey is returned after session date
                with some surveys already completed
            4) Test that multiple incompleted surveys are returned after session
                dates with some surveys already completed
            5) Test that a completed survey is not returned in the queryset
            6) Test that no surveys from a different session are returned
                in the queryset
            '''

    def setUp(self):
        self.factory = RequestFactory()
        self.ambA = AmbassadorUserFactory()
        self.ambB = AmbassadorUserFactory()
        self.tute = TuteeUserFactory()
        self.semester = SemesterFactory()
        self.course = CourseFactory()

        # Lists of individual sessions
        self.inses_listA = list()
        self.inses_listB = list()
        self.inses_listC = list()

        # Lists of individual surveys
        self.surv_listA = list()
        self.surv_listB = list()
        self.surv_listC = list()

        # Create availability for Ambassador A
        self.availA = Availability.objects.create(
                                ambassador=self.ambA,
                                semester=self.semester,
                                start_time=timezone.now(),
                                end_time=timezone.now() + timezone.timedelta(hours=1),
                                )

        # Create Availability for Ambassador A for different session
        self.availB = Availability.objects.create(
                                ambassador=self.ambA,
                                semester=self.semester,
                                start_time=timezone.now() + timezone.timedelta(days=1),
                                end_time=timezone.now() + timezone.timedelta(days=1, hours=1),
                                )

        # Create Availability for Ambassador B
        self.availC = Availability.objects.create(
                                ambassador=self.ambB,
                                semester=self.semester,
                                start_time=timezone.now(),
                                end_time=timezone.now() + timezone.timedelta(hours=1),
                                )

        # Create Session for Ambassador A with tutee
        self.sesA = Session.objects.create(
                            ambassador = self.availA.ambassador,
                            start_time = self.availA.start_time,
                            end_time = self.availA.end_time,
                            day_of_week = self.availA.day,
                            availability=self.availA,
                            tutee=self.tute,
                            course=self.course,
                            start_date=timezone.now() - timezone.timedelta(weeks=4),
                            end_date=timezone.now() + timezone.timedelta(weeks=8),
                            )

        # Create Session for Ambassador A with tutee
        self.sesB = Session.objects.create(
                            ambassador = self.availB.ambassador,
                            start_time = self.availB.start_time,
                            end_time = self.availB.end_time,
                            day_of_week = self.availB.day,
                            availability=self.availB,
                            tutee=self.tute,
                            course=self.course,
                            start_date=timezone.now() - timezone.timedelta(weeks=4),
                            end_date=timezone.now() + timezone.timedelta(weeks=8),
                            )

        # Create Session for Ambassador B with tutee
        self.sesC = Session.objects.create(
                            ambassador = self.availC.ambassador,
                            start_time = self.availC.start_time,
                            end_time = self.availC.end_time,
                            day_of_week = self.availC.day,
                            availability=self.availC,
                            tutee=self.tute,
                            course=self.course,
                            start_date=timezone.now() - timezone.timedelta(weeks=4),
                            end_date=timezone.now() + timezone.timedelta(weeks=8),
                            )

        # Create Individual Sessions for Ambassador A with tutee A and the surveys
        for i in range(4):
            self.insesA = IndividualSession.objects.create(
                    session_date=timezone.now() + timedelta(days=(i*7)),
                    session=self.sesA,
                    )
            self.inses_listA.append(self.insesA)
            self.surv_listA.append(TuteeSurvey.objects.create(individual_session=self.insesA))
            # Create Individual Sessions for Ambassador A with tutee B and the surveys
            self.insesB = IndividualSession.objects.create(
                    session_date=timezone.now() + timedelta(days=((i*7)+1)),
                    session=self.sesB,
                    )
            self.inses_listB.append(self.insesB)
            self.surv_listB.append(TuteeSurvey.objects.create(individual_session=self.insesB))
            # Create Individual Sessions for Ambassador B with tutee C and the surveys
            self.insesC = IndividualSession.objects.create(
                    session_date=timezone.now() + timedelta(days=(i*7)),
                    session=self.sesC,
                    )
            self.inses_listC.append(self.insesC)
            self.surv_listC.append(TuteeSurvey.objects.create(individual_session=self.insesC))

        self.session_pkA = self.sesA.pk



    def test_one_incompleted_survey_is_returned_after_session_date(self):
        unret_survs = self.surv_listA[1:] + self.surv_listB + self.surv_listC

        req = self.factory.get(
                '/Tutee_survey_status/{0}'.format(self.session_pkA)
        )
        req.user = self.availA.ambassador
        kwargs = { "session_pk" : self.session_pkA, }
        response = SurveyStatusListView.as_view()(req, **kwargs)
        queryset = response.context_data['object_list']

        self.assertIn(self.surv_listA[0], queryset)
        [self.assertNotIn(surv,queryset) for surv in unret_survs if surv is not None]

    @freeze_time(timezone.now() + timedelta(weeks=1))
    def test_multiple_incompleted_surveys_are_returned_after_session_dates(self):
        cs = self.surv_listA[:2]

        req = self.factory.get(
                '/Tutee_survey_status/{0}'.format(self.session_pkA)
        )
        req.user = self.availA.ambassador
        kwargs = { "session_pk" : self.session_pkA, }
        response = SurveyStatusListView.as_view()(req, **kwargs)
        queryset = response.context_data['object_list']

        c = map(repr, cs)
        self.assertQuerysetEqual(queryset, c, ordered=False)

    @freeze_time(timezone.now() + timedelta(weeks=2))
    def test_one_incompleted_survey_is_returned_after_session_dates_with_some_completed(self):
        TuteeSurvey.objects.filter(pk=self.surv_listA[0].pk).update(submitted=True)
        TuteeSurvey.objects.filter(pk=self.surv_listA[2].pk).update(submitted=True)
        self.surv_listA[0].refresh_from_db()
        self.surv_listA[2].refresh_from_db()


        req = self.factory.get(
                '/Tutee_survey_status/{0}'.format(self.session_pkA)
        )
        req.user = self.availA.ambassador
        kwargs = { "session_pk" : self.session_pkA, }
        response = SurveyStatusListView.as_view()(req, **kwargs)
        queryset = response.context_data['object_list']

        self.assertIn(self.surv_listA[1], queryset)

    @freeze_time(timezone.now() + timedelta(weeks=3))
    def test_multiple_incompleted_surveys_are_returned_after_session_dates_with_some_completed(self):
        cs = list()
        cs.append(self.surv_listA[1])
        cs.append(self.surv_listA[3])

        TuteeSurvey.objects.filter(pk=self.surv_listA[0].pk).update(submitted=True)
        TuteeSurvey.objects.filter(pk=self.surv_listA[2].pk).update(submitted=True)
        self.surv_listA[0].refresh_from_db()
        self.surv_listA[2].refresh_from_db()

        req = self.factory.get(
                '/Tutee_survey_status/{0}'.format(self.session_pkA)
        )
        req.user = self.availA.ambassador
        kwargs = { "session_pk" : self.session_pkA, }
        response = SurveyStatusListView.as_view()(req, **kwargs)
        queryset = response.context_data['object_list']

        c = map(repr, cs)
        self.assertQuerysetEqual(queryset, c, ordered=False)

    def test_that_a_completed_survey_is_not_returned_after_a_session_date(self):
        TuteeSurvey.objects.filter(pk=self.surv_listA[0].pk).update(submitted=True)
        self.surv_listA[0].refresh_from_db()

        req = self.factory.get(
                '/Tutee_survey_status/{0}'.format(self.session_pkA)
        )
        req.user = self.availA.ambassador
        kwargs = { "session_pk" : self.session_pkA, }
        response = SurveyStatusListView.as_view()(req, **kwargs)
        queryset = response.context_data['object_list']

        self.assertTrue(queryset.count() == 0)

    def test_that_surveys_from_other_sessions_are_not_returned(self):
        other_survs = TuteeSurvey.objects.filter(
            ~Q(individual_session__session__pk =
                self.surv_listA[0].individual_session.session.pk)
        )

        req = self.factory.get(
                '/Tutee_survey_status/{0}'.format(self.session_pkA)
        )
        req.user = self.availA.ambassador
        kwargs = { "session_pk" : self.session_pkA, }
        response = SurveyStatusListView.as_view()(req, **kwargs)
        queryset = response.context_data['object_list']

        for surv in other_survs:
            self.assertNotIn(surv, queryset)

