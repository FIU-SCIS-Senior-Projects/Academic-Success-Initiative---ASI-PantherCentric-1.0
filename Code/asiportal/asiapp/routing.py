from channels import route
from timesheets.consumers import (timesheet_connect,
                                  timesheet_receive,
                                  timesheet_delete,
                                  update_timesheet_submit,
                                  update_timesheet_connect)


channel_routing = [
        route('websocket.connect', timesheet_connect, path=r'^/timesheets/edit/(?P<pk>[^/]+)/stream/$'),
        route('websocket.receive', timesheet_receive, path=r'^/timesheets/edit/(?P<pk>[0-9]+)/stream/$'),
        route('websocket.receive', timesheet_delete, path=r'^/timesheets/edit/(?P<pk>[0-9]+)/delete/$'),
        route('websocket.connect', update_timesheet_connect, path=r'^/timesheets/approve/(?P<tl_name>[a-zA-Z0-9]+)/stream/$',),
        route('websocket.receive', update_timesheet_submit, path=r'^/timesheets/approve/(?P<tl_name>[a-zA-Z0-9]+)/stream/$',),
]
