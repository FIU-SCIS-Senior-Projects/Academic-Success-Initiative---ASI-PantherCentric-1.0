from django.conf.urls import url
from .views import (SubmitAvailabilityFormView,
            AvailabilityListView,
            AvailabilityUpdateView,
            AvailabilityDeleteView)

urlpatterns = [
        url(r'submit/', SubmitAvailabilityFormView.as_view(), name='submit'),
        url(r'edit/(?P<pk>\d+)', AvailabilityUpdateView.as_view(), name='edit'),
        url(r'delete/(?P<pk>\d+)', AvailabilityDeleteView.as_view(), name='delete'),
        url(r'list/', AvailabilityListView.as_view(), name='list'),
]
