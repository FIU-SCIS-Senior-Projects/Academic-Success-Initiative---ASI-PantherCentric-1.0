from django.conf.urls import url, include
from .views import (
        TeamMemberListView,
        TeamMemberDetailView,
        TeamLeaderDirectoryView,
        PollGeneratorListCreateView,
        )

urlpatterns = [

        url(r'^$',
            TeamLeaderDirectoryView.as_view(),
            name='directory'),

        url(r'^team-member-list/',
            TeamMemberListView.as_view(),
            name='team_member_list'),

        url(r'^team-member-detail/(?P<pk>\d+)',
            TeamMemberDetailView.as_view(),
            name='team_member_detail'),

        url(r'^poll-generator/',
            PollGeneratorListCreateView.as_view(),
            name='poll_generator_time'),
        ]
