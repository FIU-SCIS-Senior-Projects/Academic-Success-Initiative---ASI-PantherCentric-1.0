from django.conf.urls import url
from .views import CourseListView
urlpatterns = [
    url('course-list/', CourseListView.as_view(), name='course_list'),
]
