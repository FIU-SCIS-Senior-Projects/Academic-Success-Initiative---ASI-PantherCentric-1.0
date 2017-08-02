# Django
from django.conf.urls import url

# Local Django
from .views import UpdateOrCreateHourLimitView

urlpatterns = [
        url(r'update-restrictions/$', UpdateOrCreateHourLimitView.as_view(), name='update_or_create_form'),
]

