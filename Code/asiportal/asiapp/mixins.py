from django.http import HttpResponseRedirect

class LoginRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return super(LoginRequiredMixin, self)\
                    .dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')

class ProjectPermRequired(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm('timesheets.approve_timesheet'):
            return super(ProjectPermRequired, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')

class AmbassadorPermRequired(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm('timesheets.add_timesheet'):
            return super(AmbassadorPermRequired, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')
