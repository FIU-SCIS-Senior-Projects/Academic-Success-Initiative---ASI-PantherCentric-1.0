from collections import defaultdict
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import generic
from tutoring_sessions.models import Session, IndividualSession
from surveys.models import AmbassadorSurvey, TuteeSurvey
from admindashboard.services.averager import gather_context
from admindashboard.models import Note
from django import forms
from admindashboard.forms import NoteForm

class StudentDetailView(generic.DetailView):
    model = User
    template_name = 'admindashboard/studentdetails.html'
    form_class = NoteForm

    def get_object(self, queryset=None):
        obj = User.objects.get(username=self.kwargs.get('username'))
        return obj

    def get_context_data(self, **kwargs):
        context = super(StudentDetailView, self).get_context_data(**kwargs)
        context['courses'] = [session.course for session in self.object.sessions.distinct('course')]
        context['notes'] = self.object.notes.all()
        context['note_form'] = NoteForm(initial={'tutee': self.object.get_username()})
        return context

    def form_valid(self, form, **kwargs):
        obj = form.save(commit=False)
        obj.user = self.object.get_username()
        obj.save()
        return self.render_to_response(self.get_context_data(**kwargs))

    def form_invalid(self, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()

        if 'notes' in request.POST:

            # get the primary form
            form_class = self.form_class()
            form_name = 'notes'

        # else:

        #     # get the secondary form
        #     form_class = self.second_form_class
        #     form_name = 'form2'

        # get the form
        form = self.form_class(request.POST)

        # validate
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(**{form_name: form})

class AdminDashboardView(generic.TemplateView):
    template_name = 'admindashboard/admindashboard.html'

    def get_context_data(self, **kwargs):
        context = super(AdminDashboardView, self).get_context_data(**kwargs)
        sessions = Session.objects.prefetch_related('tutee', 'course').all()
        inter = defaultdict(list)
        for session in sessions:
            inter[session.tutee] +=  [session.course] if session.course not in inter[session.tutee] else []
        context['tutees'] = inter.items
        return context

class SurveyByCourseStatisticsView(generic.ListView):
    model = Session
    template_name = 'admindashboard/surveysbycourse.html'

    def get_context_data(self, **kwargs):
        # limit queries to a student and a course
        context = dict()
        sessions = Session.objects.filter(
                tutee__username=self.kwargs.get('username'),
                course__slug=self.kwargs.get('course_slug'),
                )
        context['sessions'] = gather_context(sessions)
        return context
