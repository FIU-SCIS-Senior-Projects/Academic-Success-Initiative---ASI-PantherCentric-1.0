from django.conf.urls import url
from .views import ProjectTSEntryCreateView, ProjectTSApprovalView

urlpatterns = [
        url(r'create/$', ProjectTSEntryCreateView.as_view(),
            name='project_timesheet_create'),
        url(r'list/$', ProjectTSApprovalView,
            name='project_list_view'),
]
