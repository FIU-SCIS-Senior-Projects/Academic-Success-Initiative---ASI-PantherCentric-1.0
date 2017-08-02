from django.conf.urls import url
from .views import (
        RequestTutoringFormView,
        UpdateTutoringRequestFormView,
        TutoringRequestListView,
        TutoringRequestCreateView,
        SessionCancelationRequestCreateView,
        SessionCancelationRequestListView,
        SessionCancelationRequestUpdateView,
        RequestSuccessView,
        RequestDirectoryView,
        )

urlpatterns = [
    url(r'^$', RequestDirectoryView.as_view(), name='directory'),
    url(r'request-tutoring/success/$', RequestSuccessView.as_view(),name='request_success'),
    url(r'request-tutoring/(?P<course>[-\w\d]+)/(?P<semester>[-\w\d]+)', RequestTutoringFormView.as_view(),name='request_tutoring'),
    url(r'requests/request-list/update/(?P<pk>\d+)', UpdateTutoringRequestFormView.as_view(),name='update_request'),
    url(r'requests/tutoring-request-list/$', TutoringRequestListView.as_view(),name='tutoring_request_list'),
    url(r'requests/tutoring-request-list/(?P<order>[A-D])/$', TutoringRequestListView.as_view(),name='tutoring_request_list_filtered'),
    url(r'requests/create', TutoringRequestCreateView.as_view(), name='create'),
    url(r'requests/cancel-session', SessionCancelationRequestCreateView.as_view(), name='cancel_session_form'),
    url(r'requests/session-cancelation-requests/update/(?P<pk>\d+)',
        SessionCancelationRequestUpdateView.as_view(),
        name='session_cancelation_update'),
    url(r'requests/session-cancelation-requests', SessionCancelationRequestListView.as_view(), name='session_cancelation_requests'),

]
