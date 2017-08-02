from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from django.views.generic.edit import ModelFormMixin
from django.views import generic
from courses.models import Course
from .models import PollTime
from .forms import PollGeneratorListCreateForm, PollGeneratorFormSet
from .services import get_survey_stats_for_ambassador
from tutoring_sessions.models import Availability, Session

class TeamLeaderDirectoryView(generic.TemplateView):
    template_name = 'team_leader_tools/directory.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm('team_leader_tools.change_polltime'):
            return super(TeamLeaderDirectoryView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')

class TeamMemberListView(generic.ListView):
    template_name = 'team_leader_tools/member_list.html'
    model = User

    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm('team_leader_tools.change_polltime'):
            return super(TeamMemberListView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')

    def get_queryset(self):
        courses = self.request.user.teams.all()
        team_pks = [c.get_team_pks() for c in courses]
        team_pks = [item for sublist in team_pks for item in sublist]
        # make sure to only get users team members and not the user themselves
        queryset = User.objects.filter(pk__in=team_pks)
        return queryset

class TeamMemberDetailView(generic.DetailView):
    model = User
    template_name = 'team_leader_tools/member_detail.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm('team_leader_tools.change_polltime'):
            return super(TeamMemberDetailView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')

    def get_context_data(self, **kwargs):
        context_data = super(TeamMemberDetailView, self).get_context_data(**kwargs)
        context_data['sessions'] = Session.objects.filter(
                availability__ambassador = self.object,
                course__team_leader=self.request.user,
                )
        context_data['survey_stats'] = get_survey_stats_for_ambassador(
                context_data['sessions'])
        context_data['available_times'] = Availability.objects.filter(
                ambassador = self.object,
                is_scheduled = False)
        return context_data

#Create an available time for a group session to make a poll for
class PollGeneratorListCreateView(generic.ListView, ModelFormMixin):
    model = PollTime
    form_class = PollGeneratorListCreateForm
    template_name = 'team_leader_tools/poll_generator_times.html'

    def form_valid(self, form):
        print("in form valid")
        time = form.save(commit=False)
        time.save()
        return super(PollGeneratorListCreateView, self).form_valid(form)

    def get_queryset(self):
        queryset = []
        tlcourses = self.request.user.teams.all()
        zipped = [zip([tlcourse],[PollTime.objects.filter(course__name=tlcourse.name)]) for tlcourse in tlcourses ]
        [queryset.append(list(z)) for z in zipped]
        return queryset

    def get(self, request, *args, **kwargs):
        print(request.method)
        self.object = None
        self.form = self.get_form(self.form_class)
        # Explicitly states what get to call:
        return generic.ListView.get(self, request, *args, **kwargs)

    # Took this from jakes formset post. Work in progress
    def post(self, request, *args, **kwargs):
        print(request.method)
        formset = PollGeneratorFormSet(request.POST)
        ignore_forms = formset.deleted_forms
        to_post = [form for form in formset.forms if form not in ignore_forms]
        self.object = None
        if formset.is_valid():
            for form in to_post:
                    if form.is_valid():
                        print("formvalid")
                        self.object = self.form.save()
        return self.get(request, *args, **kwargs)

#    Works for posting one form
#    def post(self, request, *args, **kwargs):
#        print(request.method)
#        # When the form is submitted, it will enter here
#        self.object = None
#        self.form = self.get_form(self.form_class)
#
#        if self.form.is_valid():
#            print("formvalid")
#            self.object = self.form.save()
#
#        return self.get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(PollGeneratorListCreateView, self).get_context_data(*args, **kwargs)
        context['form'] = self.form
        return context




