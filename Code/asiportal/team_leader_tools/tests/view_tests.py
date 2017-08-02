from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from courses.models import Course
from team_leader_tools.views import (
        TeamMemberListView,
        TeamMemberDetailView)

class CommonView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username='tl', is_superuser=True)

class TeamMemberListViewTest(CommonView):

    def setUp(self):
        super(TeamMemberListViewTest, self).setUp()
        self.course = Course.objects.create(
                name='MAD3305',
                team_leader=self.user)
        # make sure at least 1 person on team
        self.member1 = User.objects.create(username='member1')
        self.course.team.add(self.member1)
        self.course.team.add(self.user)

    def test_that_team_members_can_be_seen(self):
        request = self.factory.get('/')
        request.user = self.user
        response = TeamMemberListView.as_view()(request)
        team = response.context_data['object_list']
        self.assertTrue(team)
        self.assertIn(self.member1, team)

    def test_that_only_team_members_are_in_queryset(self):
        not_in = User.objects.create(username='not_in')
        request = self.factory.get('/')
        request.user = self.user
        response = TeamMemberListView.as_view()(request)
        team = response.context_data['object_list']
        self.assertTrue(team)
        self.assertIn(self.member1, team)
        self.assertNotIn(not_in, team)

class TeamMemberDetailViewTest(CommonView):
    def test_that_view_werks(self):
        request = self.factory.get('/')
        request.user = self.user
        kwargs = { 'pk' : self.user.pk }
        response = TeamMemberDetailView.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 200)
