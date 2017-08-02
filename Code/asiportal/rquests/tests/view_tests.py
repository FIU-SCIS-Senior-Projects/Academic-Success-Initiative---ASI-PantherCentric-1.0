from datetime import timedelta
from mock import patch, MagicMock
from django.contrib.auth.models import User, AnonymousUser
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
from django.template.loader import render_to_string
from django.utils import timezone
from availabilities.models import Availability
from availabilities.tests.factory import AvailabilityFactory
from courses.models import Course
from semesters.models import Semester
from rquests.forms import RequestTutoringForm
from rquests.models import (
        TutoringRequest,
        SessionCancelationRequest)
from rquests.views import (RequestTutoringFormView,
                            UpdateTutoringRequestFormView,
                            TutoringRequestCreateView,
                            SessionCancelationRequestCreateView,
                            SessionCancelationRequestUpdateView,
                            TutoringRequestListView,)
from tutoring_sessions.models import (
                                Session,
                                IndividualSession)
from surveys.models import AmbassadorSurvey, TuteeSurvey

def setup_view(view, request, *args, **kwargs):
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view

class SummerSituationsTest(TestCase):
    def setUp(self):
        self.tut = User.objects.create(username='john',
                                       first_name='John',
                                       last_name='Doe',)
        self.tut.set_password('password')
        self.tut.save()
        self.amb = User.objects.create(username='amb')
        self.course = Course.objects.create(name='MAC2311', team_leader = self.amb)
        self.summC = Semester.objects.create(term='SC',
                    start_date=timezone.now(),
                    end_date = timezone.now() + timedelta(weeks=12),
                    )
        self.summB = Semester.objects.create(term='SB',
                    start_date=timezone.now()+timedelta(weeks=6),
                    end_date = timezone.now() + timedelta(weeks=12),
                    )
        self.summA = Semester.objects.create(term='SA',
                    start_date=timezone.now(),
                    end_date = timezone.now() + timedelta(weeks=6),
                    )
        self.factory = RequestFactory()

    def test_summc_updates_a_and_b(self):
        ambassador = User.objects.create(username='jane',
                                         first_name='Jane',
                                         last_name='Doe')
        self.course.team.add(ambassador)
        availability = AvailabilityFactory(ambassador=ambassador,
                                        semester=self.summC)
        availb = AvailabilityFactory(ambassador=ambassador,
                                        semester=self.summB)
        availa = AvailabilityFactory(ambassador=ambassador,
                                        semester=self.summA)
        kwargs = {'course' : self.course.slug,
                  'semester' : self.summC.slug,
                  }
        data = {'availability' : availability.id}
        request = self.factory.post(reverse('requests:request_tutoring',
                                    kwargs=kwargs), data)
        request.user = self.tut
        response = RequestTutoringFormView.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)
        aAvail = Availability.objects.get(semester=self.summA)
        bAvail = Availability.objects.get(semester=self.summB)
        self.assertTrue(aAvail.is_scheduled)
        self.assertTrue(bAvail.is_scheduled)

    def test_summa_updates_c(self):
        ambassador = User.objects.create(username='jane',
                                         first_name='Jane',
                                         last_name='Doe')
        self.course.team.add(ambassador)
        availability = AvailabilityFactory(ambassador=ambassador,
                                        semester=self.summA)
        availb = AvailabilityFactory(ambassador=ambassador,
                                        semester=self.summB)
        availa = AvailabilityFactory(ambassador=ambassador,
                                        semester=self.summC)
        kwargs = {'course' : self.course.slug,
                  'semester' : self.summA.slug,
                  }
        data = {'availability' : availability.id}
        request = self.factory.post(reverse('requests:request_tutoring',
                                    kwargs=kwargs), data)
        request.user = self.tut
        response = RequestTutoringFormView.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)
        cAvail = Availability.objects.get(semester=self.summC)
        bAvail = Availability.objects.get(semester=self.summB)
        self.assertTrue(cAvail.is_scheduled)
        self.assertFalse(bAvail.is_scheduled)

    def test_summb_updates_c(self):
        ambassador = User.objects.create(username='jane',
                                         first_name='Jane',
                                         last_name='Doe')
        self.course.team.add(ambassador)
        availability = AvailabilityFactory(ambassador=ambassador,
                                        semester=self.summB)
        availb = AvailabilityFactory(ambassador=ambassador,
                                        semester=self.summA)
        availa = AvailabilityFactory(ambassador=ambassador,
                                        semester=self.summC)
        kwargs = {'course' : self.course.slug,
                  'semester' : self.summB.slug,
                  }
        data = {'availability' : availability.id}
        request = self.factory.post(reverse('requests:request_tutoring',
                                    kwargs=kwargs), data)
        request.user = self.tut
        response = RequestTutoringFormView.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)
        cAvail = Availability.objects.get(semester=self.summC)
        aAvail = Availability.objects.get(semester=self.summA)
        self.assertTrue(cAvail.is_scheduled)
        self.assertFalse(aAvail.is_scheduled)

class RequestTutoringFormViewTest(TestCase):
    def setUp(self):
        self.tut = User.objects.create(username='john',
                                       first_name='John',
                                       last_name='Doe',)
        self.tut.set_password('password')
        self.tut.save()
        amb = User.objects.create(username='djdookie')
        self.course = Course.objects.create(name='MAC2311', team_leader=amb)
        self.semester = Semester.objects.create()
        self.summC = Semester.objects.create(term='SC',
                    start_date=timezone.now(),
                    end_date = timezone.now() + timedelta(weeks=12),
                    )
        self.factory = RequestFactory()

    def test_authenticated_users_can_view_page(self):
        request = self.factory.get('requests/request-tutoring/%s'%
                                    (self.course.name))
        request.user = self.tut
        response = RequestTutoringFormView.as_view()\
                (request, course=self.course.slug,
                        semester=self.semester.slug)
        self.assertEqual(response.status_code, 200)

    def test_non_authenticated_users_get_redirected(self):
        request = self.factory.get('requests/request-tutoring/%s' % 
                                     (self.course.name))
        request.user = AnonymousUser()
        response = RequestTutoringFormView.as_view()\
            (request, kwargs={"course" : self.course, "semester" : self.semester})
        self.assertEqual(response.status_code, 302)

    @patch('rquests.models.TutoringRequest.save', MagicMock(name='save'))
    def test_forms_can_be_submitted(self):
        ambassador = User.objects.create(username='jane',
                                         first_name='Jane',
                                         last_name='Doe')
        self.course.team.add(ambassador)
        availability = AvailabilityFactory(ambassador=ambassador,
                                        semester=self.semester)
        kwargs = {'course' : self.course.slug,
                  'semester' : self.semester.slug,
                  }
        data = {'availability' : availability.id}
        request = self.factory.post(reverse('requests:request_tutoring',
                                    kwargs=kwargs), data)
        request.user = self.tut
        response = RequestTutoringFormView.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(TutoringRequest.save.called)
        self.assertEqual(TutoringRequest.save.call_count, 1)

class UpdateRequestTutoringFormViewTest(TestCase):

    def setUp(self):
        self.sem = Semester.objects.create(
                start_date=timezone.now(),
                end_date=timezone.now()+timedelta(weeks=12))
        self.user = User.objects.create(username='ambassador', is_superuser=True)
        self.factory = RequestFactory()
        self.amb = User.objects.create(username='john',
                                       first_name='John',
                                       last_name='Doe')
        self.ava = AvailabilityFactory(ambassador=self.amb,
                                       semester=self.sem)
        self.course = Course.objects.create(name='MAC2311', team_leader = self.amb)
        self.course.team.add(self.amb)
        self.tr = TutoringRequest.objects.create(availability=self.ava,
                                            submitted_by=self.amb,
                                            course=self.course)

    def test_view_is_accessible_by_authorized_users_only(self):
        request = self.factory.get('/some-url/')
        kwargs = {'pk' : self.tr.pk}
        request.user = self.user
        response = UpdateTutoringRequestFormView.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 200)
    
    def test_view_is_unaccessible_by_authorized_users_only(self):
        kwargs = {'pk' : self.tr.pk}
        request = self.factory.get('/some-url/', pk=self.tr.pk)
        request.user = AnonymousUser()
        response = UpdateTutoringRequestFormView.as_view()(request, )
        self.assertEqual(response.status_code, 302)

    def test_view_creates_sessions_with_correct_tutoring_request(self):
        data = {'status' : 'B',
                'room_number' : '101A',
                }
        kwargs = {'pk' : self.tr.pk}
        request = self.factory.post('/some-url/', data)
        request.user = self.user
        response = UpdateTutoringRequestFormView.as_view()(request,
                                                           **kwargs)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Session.objects.all())
        self.assertTrue(IndividualSession.objects.all())

    def test_view_updates_request_as_being_scheduled(self):
        data = {'status' : 'B',
                'room_number' : '101A',
                }
        kwargs = {'pk' : self.tr.pk}
        request = self.factory.post('/some-url/', data)
        request.user = self.user
        response = UpdateTutoringRequestFormView.as_view()(request,
                                                           **kwargs)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Session.objects.all())
        q = TutoringRequest.objects.get(status='B')
        self.assertEqual(q, self.tr)

    def test_view_can_update_request_and_not_create_session(self):
        data = {'status' : 'C',
                'room_number' : '101A',
                }
        kwargs = {'pk' : self.tr.pk}
        request = self.factory.post('/some-url/', data)
        request.user = self.user
        response = UpdateTutoringRequestFormView.as_view()(request,
                                                           **kwargs)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Session.objects.all())
        q = TutoringRequest.objects.get(status='C')
        self.assertEqual(q, self.tr)

    def test_no_room_available_sets_other_times_as_unavailable(self):
        data = {'status' : 'D',
                'room_number' : '101A',
                }
        kwargs = {'pk' : self.tr.pk}
        amb2 = User.objects.create(username='foo')
        ava2 = AvailabilityFactory(ambassador=amb2,
                                    semester=self.sem,)
        request = self.factory.post('/some-url/', data)
        request.user = self.user
        response = UpdateTutoringRequestFormView.as_view()(request,
                                                           **kwargs)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Session.objects.all())
        q = TutoringRequest.objects.get(status='D')
        self.assertEqual(q, self.tr)
        no_rooms = Availability.objects.filter(room_available=False)
        self.assertIn(self.ava, no_rooms)
        self.assertIn(ava2, no_rooms)

class TutoringRequestListViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.sem = Semester.objects.create()
        self.amb = User.objects.create(username='john',
                                       first_name='John',
                                       last_name='Doe',
                                       is_superuser=True)
        self.ava = AvailabilityFactory(ambassador=self.amb,
                                       semester=self.sem)
        self.course = Course.objects.create(name='MAC2311', team_leader=self.amb)
        self.course.team.add(self.amb)

    def test_view_has_requests(self):
        t = TutoringRequest.objects.create(availability=self.ava,
                                       submitted_by = self.amb,
                                       course=self.course)
        request = self.factory.get('/')
        request.user = self.amb
        view = TutoringRequestListView()
        view = setup_view(view, request)
        self.assertIn(t, view.get_queryset())

class TutoringRequestCreateViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_that_requests_can_be_made(self):
        amb = User.objects.create(username='amb', is_superuser=True)
        tut = User.objects.create(username='tut')
        sem = Semester.objects.create(
                start_date=timezone.now(),
                end_date = timezone.now() + timedelta(weeks=12),
                )
        availability = Availability.objects.create(
                semester = sem,
                ambassador = amb,
                start_time = '11:00:00',
                end_time = '12:00:00',
                day = 1,
                )
        course = Course.objects.create(name='MAD3305',team_leader=amb)
        course.team.add(amb)
        data = {
                'availability' : availability.pk,
                'submitted_by' : tut.pk,
                'course' : course.pk,
                }
        request = self.factory.post('/', data)
        request.user = amb
        response = TutoringRequestCreateView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(TutoringRequest.objects.all())

class SessionCancelSetUp(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.amb = User.objects.create(username='amb', is_superuser=True)
        self.tut = User.objects.create(username='tut')
        self.sem = Semester.objects.create(
                start_date=timezone.now(),
                end_date = timezone.now() + timedelta(weeks=12),
                )
        self.availability = Availability.objects.create(
                semester = self.sem,
                ambassador = self.amb,
                start_time = '11:00:00',
                end_time = '12:00:00',
                day = 1,
                )
        self.course = Course.objects.create(name='MAD3305',team_leader=self.amb)
        self.session = Session.objects.create(
                ambassador = self.availability.ambassador,
                start_time = self.availability.start_time,
                end_time = self.availability.end_time,
                day_of_week = self.availability.day,
                availability = self.availability,
                tutee = self.tut,
                course = self.course,
                start_date = timezone.now(),
                end_date = timezone.now() + timedelta(weeks=5),
                )

class SessionCancelationRequestCreateViewTest(SessionCancelSetUp):
    def test_that_requests_can_be_made(self):
        data = {
                'session' : self.session.pk,
                'reason' : 'Excessive absences',
                }
        request = self.factory.post('/', data)
        request.user = self.amb
        response = SessionCancelationRequestCreateView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(SessionCancelationRequest.objects.all())

class SessionCancelationRequestUpdateViewTest(SessionCancelSetUp):

    def setUp(self):
        super(SessionCancelationRequestUpdateViewTest,self).setUp()
        self.cancel_request = SessionCancelationRequest.objects.create(
                session=self.session,
                reason='This guys a cunt',
                )
        dates = self.session.get_dates()
        inds = IndividualSession.make_from_dates(self.session, dates)
        AmbassadorSurvey.create_surveys_from_individual_sessions(inds)
        TuteeSurvey.create_surveys_from_individual_sessions(inds)


    def test_that_cancelation_requests_can_be_completed(self):
        data = {
                'status' : 'B',
                }
        kwargs = {'pk' : self.cancel_request.pk }
        request = self.factory.post('/', data)
        request.user = self.amb
        response = SessionCancelationRequestUpdateView.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(SessionCancelationRequest.objects.filter(status='B'))

    def test_that_cancelation_requests_remove_all_further_sessions(self):
        data = {
                'status' : 'B',
                }
        kwargs = {'pk' : self.cancel_request.pk }
        request = self.factory.post('/', data)
        request.user = self.amb
        response = SessionCancelationRequestUpdateView.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(SessionCancelationRequest.objects.filter(status='B'))
        updated_session = Session.objects.get(pk=self.session.pk)
        updated_request = SessionCancelationRequest.objects.get()
        self.assertEqual(updated_session.end_date, updated_request.submitted_at.date())
        self.assertFalse(
            IndividualSession.objects.filter(session_date__gte=timezone.now())
            )

    def test_that_cancelation_requests_remove_all_surveys_after_end_date(self):
        data = {
                'status' : 'B',
                }
        kwargs = {'pk' : self.cancel_request.pk }
        request = self.factory.post('/', data)
        request.user = self.amb
        response = SessionCancelationRequestUpdateView.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(SessionCancelationRequest.objects.filter(status='B'))
        self.assertFalse(
            AmbassadorSurvey.objects.filter(
                individual_session__session_date__gte=timezone.now())
            )
        self.assertFalse(
            TuteeSurvey.objects.filter(
                individual_session__session_date__gte=timezone.now())
            )
    def test_that_cancelation_requests_remove_all_surveys_after_end_date(self):
        data = {
                'status' : 'B',
                }
        kwargs = {'pk' : self.cancel_request.pk }
        request = self.factory.post('/', data)
        request.user = self.amb
        response = SessionCancelationRequestUpdateView.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(SessionCancelationRequest.objects.filter(status='B'))
        self.assertFalse(
            AmbassadorSurvey.objects.filter(
                individual_session__session_date__gte=timezone.now())
            )
        self.assertFalse(
            TuteeSurvey.objects.filter(
                individual_session__session_date__gte=timezone.now())
            )
