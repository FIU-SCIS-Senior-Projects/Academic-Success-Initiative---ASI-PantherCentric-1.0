from django.conf.urls import url
from .views import (
        UserProfileCreateView,
        UserProfileUpdateView,
        UserProfileDetailView,
        )

urlpatterns = [
        url(r'^create/$', UserProfileCreateView.as_view(), name='create'),
        url(r'^detail/(?P<pk>[0-9]+)/$', UserProfileDetailView.as_view(), name='detail'),
        url(r'^update/(?P<pk>[0-9]+)/$', UserProfileUpdateView.as_view(), name='update'),

        ]
