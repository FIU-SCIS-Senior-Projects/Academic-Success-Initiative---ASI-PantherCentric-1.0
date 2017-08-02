from django.conf.urls import url
from .views import (TimeSheetListView,
                    FinalApproveAmbassadorTimeSheet,
                    TimeSheetAmbassadorListView,
                    AmbassadorListView,
                    TimeSheetDetailView,
                    TimeSheetCreateFormView,
                    edit_timesheet,
                    approve_timesheet,
                    download_timesheet,
                    )

urlpatterns = [
        url(r'list/$', TimeSheetListView.as_view(), name='timesheet_list'),
        url(r'edit/(?P<timesheet_pk>[0-9]+)/$', edit_timesheet, name='edit_timesheet'),
        url(r'create/$', TimeSheetCreateFormView.as_view(), name='new_timesheet'),
        url(r'approve/$', approve_timesheet, name='approve'),
        url(r'ambassadors/$', AmbassadorListView.as_view(), name='ambassador_list'),
        url(r'ambassadors/(?P<ambassador>[a-zA-Z0-9]+)/timesheets/$', TimeSheetAmbassadorListView.as_view(), name='ambassador_sheets'), 
        url(r'ambassadors/timesheets/approve/(?P<ambassador>[a-zA-Z0-9]+)/(?P<pk>[0-9]+)/$', FinalApproveAmbassadorTimeSheet.as_view(), name='final_approve'),
        url(r'ambassadors/(?P<ambassador>[a-zA-Z0-9]+)/timesheets/(?P<pk>[0-9]+)/download/$', download_timesheet, name='download_final'),
        url(r'detail/(?P<timesheet_pk>[0-9]+)/$', TimeSheetDetailView.as_view(), name='timesheet_detail')
        ]
