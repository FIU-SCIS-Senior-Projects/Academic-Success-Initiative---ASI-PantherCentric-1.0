from django.contrib.auth.models import User, AnonymousUser
from django.template.loader import render_to_string
from django.test import TestCase, RequestFactory
from courses.models import Course
from courses.views import CourseListView
from semesters.models import Semester

class CourseListViewTest(TestCase):
    def setUp(self):
        self.tut = User.objects.create(username='john',
                                       first_name='John',
                                       last_name='Doe')
        self.tut.set_password('pass')
        self.tut.save()
        self.factory = RequestFactory()
        self.sem = Semester.objects.create()
        self.tl = User.objects.create(username='some_guy')
        self.c = Course.objects.create(name='MAC2311', team_leader=self.tl)

    def test_anonymous_cant_access_the_course_list(self):
        request = self.factory.get('/courses/course-list/')
        request.user = AnonymousUser()
        response = CourseListView.as_view()(request)
        self.assertEqual(response.status_code, 302)

    def test_john_can_access_the_course_list(self):
        request = self.factory.get('/courses/course-list/')
        request.user = self.tut
        response = CourseListView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_courses_with_no_ambassadors_are_not_shown(self):
        c = Course.objects.create(name='MAC2311', professor='Idris Mercer', team_leader=self.tl)
        response = CourseListView()
        self.assertFalse(response.get_queryset())

    def test_courses_with_ambassadors_are_shown(self):
        self.c.team.add(self.tut)
        response = CourseListView()
        self.assertTrue(response.get_queryset())

    def test_semesters_are_loaded(self):
        Semester.objects.create()
        self.c.team.add(self.tut)
        request = self.factory.get('/courses/course-list/')
        request.user = self.tut
        response = CourseListView.as_view()(request)
        self.assertTrue(response.context_data['semesters'])

    def test_html_is_rendered_correctly(self):
        self.c.team.add(self.tut)
        request = self.factory.get('/courses/course-list/')
        request.user = self.tut
        response = CourseListView.as_view()(request)
        context = {'object_list' : [self.c],
                   'semesters': [self.sem],
                   'request' : request}
        expected_html = render_to_string('courses/course_list.html',
                                        context = context)
        response.render()
        self.assertEqual(response.content.decode(), expected_html)
