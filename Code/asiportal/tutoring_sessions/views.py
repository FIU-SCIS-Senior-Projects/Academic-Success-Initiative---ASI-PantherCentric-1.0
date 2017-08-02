import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from tutoring_sessions.models import Session, IndividualSession
from .forms import TutoringSessionUpdateForm, TimeSheetForm
# should update a tutoring session with some new info
class TutoringSessionUpdateView(generic.UpdateView):
    model = Session
    form_class = TutoringSessionUpdateForm
    success_url = reverse_lazy('home')
    template_name = 'tutoring_sessions/edit_session_form.html'

    def form_valid(self, form):
        # duplicate the availability and session
        # swap all future individual sessions
        s = Session.duplicate_for_swap(form)
        IndividualSession.swap_sessions_with_form(s, form)
        return super(TutoringSessionUpdateView, self).form_valid(form)

class TutoringSessionListView(generic.ListView):
    model = Session

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return super(TutoringSessionListView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse_lazy('login'))

    def get_queryset(self):
        queryset = Session.objects.filter(
                Q(availability__ambassador = self.request.user) | Q(tutee = self.request.user),
                end_date__gte=timezone.now(),
                )
        return queryset

# this is okay. but its kind of bad.
# what we're gonna do is make a form that creates one of these guys with a start - end date so 
# we can get the correct total amount of sessions
class CreateTimeSheetFormView(generic.FormView):
    form_class = TimeSheetForm
    success_url = None
    template_name = 'tutoring_sessions/timesheet.html'
