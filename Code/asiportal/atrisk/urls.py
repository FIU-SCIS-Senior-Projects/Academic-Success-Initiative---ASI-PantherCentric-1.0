from django.conf.urls import url
from .views import (
        LandingView, 
        ViewCountView,
        StudentVideoListView,
        StudentAccountCreationView,
        AdvisorVideoListView,
        SuccessView,
        VideoView )

urlpatterns = [
        url(r'dir/$', LandingView.as_view(), name='landing'),
        url(r'video/(?P<urlcode>[a-zA-Z0-9\-\_]+)$', VideoView.as_view(), name='video_view'),
        url(r'total-views/(?P<urlcode>[a-zA-Z0-9\-\_]+)$', ViewCountView.as_view(), name='view_count_view'),
        url(r'video-list/$', StudentVideoListView.as_view(), name='student_video_list'),
        url(r'create/student-acct/$', StudentAccountCreationView.as_view(), name='create_alt_acct'),
        url(r'video-list/a/$', AdvisorVideoListView.as_view(), name='advisor_video_list'),
        url(r'create/student-acct/success$', SuccessView.as_view(), name='success'),
        ]
