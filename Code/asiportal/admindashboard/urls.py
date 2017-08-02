from django.conf.urls import url
from .views import (
        AdminDashboardView,
        StudentDetailView,
        SurveyByCourseStatisticsView
        )

urlpatterns = [
    url(r'^$', AdminDashboardView.as_view(), name='home'),
    url(r'^student/detail/(?P<username>[\w\d]+)$', StudentDetailView.as_view(), name='student_detail'),
    url(r'^student/detail/(?P<username>[\w\d]+)/surveysbycourse/(?P<course_slug>[-\w]+)$', SurveyByCourseStatisticsView.as_view(), name='surveys_by_course')
]
