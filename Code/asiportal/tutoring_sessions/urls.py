from django.conf.urls import url
from .views import (
        TutoringSessionUpdateView,
        TutoringSessionListView,
        )

urlpatterns = [
    url(r'^edit-session/(?P<pk>\d+)', TutoringSessionUpdateView.as_view(),
        name='edit_session'),
    url(r'^list-sessions/$', TutoringSessionListView.as_view(),
        name='list'),
        ]
