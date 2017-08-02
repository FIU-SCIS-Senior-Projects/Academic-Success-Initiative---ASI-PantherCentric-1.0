from django.test import TestCase
from courses.models import Course
from django.contrib.auth.models import User

class CourseTest(TestCase):
    def test_course_is_represented_correctly(self):
        amb = User.objects.create(username='some_guy')
        c = Course.objects.create(name='MAC2311', team_leader=amb)
        self.assertEqual(c.__str__(), 'MAC2311')
