from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from .views import (
        HomePageView,
        LoginView,
        log_out,
        ActivateAccountView,
        CreateAccountFormView,
        ProfileDirectoryView,
        AccountSuccessTemplateView,
        )
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^accounts/register$', CreateAccountFormView.as_view(), name='create_account'),

    url(r'^accounts/register/success$', AccountSuccessTemplateView.as_view(), name='account_success'),
    url(r'^accounts/reset-password/$',
        auth_views.password_reset,
        { 'template_name' : 'password_reset.html' },
        name='password_reset',

        ),

    url(r'^accounts/reset-password/done/$',
        auth_views.password_reset_done,
        { 'template_name' : 'password_reset_done.html',},
       name='password_reset_done', ),

    url(
        r'^accounts/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm,
        { 'template_name' : 'password_reset_confirm.html' },
        name='password_reset_confirm',
        ),

    url(r'^accounts/reset/done/$', auth_views.password_reset_complete,
        { 'template_name' : 'password_reset_complete.html' },
        name='password_reset_complete',
        ),
    url(r'^accounts/activate/(?P<token>[0-9A-Za-z_\-]+)/$',
        ActivateAccountView.as_view(), name='activate_account'),
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', log_out, name='logout'),
    url(r'^courses/', include('courses.urls', namespace='courses')),
    url(r'^requests/', include('rquests.urls', namespace='requests')),
    url(r'^availabilities/', include('availabilities.urls', namespace='availabilities')),
    url(r'^tutoring-sessions/', include('tutoring_sessions.urls',
        namespace='tutoring_sessions')),
    url(r'^surveys/', include('surveys.urls', namespace='surveys')),
    url(r'^team-leader-tools/', include('team_leader_tools.urls',
        namespace='team_leader_tools')),
    url(r'^reports/', include('reports.urls', namespace='reports')),
    url(r'^restrictions/', include('restrictions.urls', namespace='restrictions')),
    url(r'^ar/', include('atrisk.urls', namespace='atrisk')),
    url(r'^profile/', ProfileDirectoryView.as_view(), name='profile'),
    url(r'^projects/', include('projects.urls', namespace='projects')),
    url(r'^timesheets/', include('timesheets.urls', namespace='timesheets')),
    url(r'^my-profile/', include('user_profiles.urls', namespace='user_profiles')),
    url(r'^admindashboard/', include('admindashboard.urls', namespace='admin_dashboard')),

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
