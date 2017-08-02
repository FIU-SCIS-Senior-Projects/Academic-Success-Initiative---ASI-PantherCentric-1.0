from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.views.generic.edit import ModelFormMixin
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.forms import modelformset_factory
from .models import ProjectTSEntry, ProjectTS
from .forms import ProjectTSModelForm, ProjectFormSet, ProjectTSEntryApprovalForm

class ProjectTSEntryCreateView(generic.CreateView):
    model = ProjectTS
    form_class = ProjectTSModelForm
    template_name = 'project_times.html'
    success_url = '/profile/'

    def get(self, request, *args, **kwarg):
        try:
            self.timesheet = ProjectTS.objects.get(
                    pay_period_begin__lte=timezone.now(),
                    pay_period_end__gte=timezone.now(),
                    ambassador=self.request.user)
        except ProjectTS.DoesNotExist:
            self.timesheet = None

        self.object = None
        if self.timesheet:
            timesheet_form = ProjectTSModelForm(instance=self.timesheet)
            timesheet_entry_formset = ProjectFormSet(instance=self.timesheet)
        else:
            timesheet_form = ProjectTSModelForm()
            timesheet_entry_formset = ProjectFormSet()
        return self.render_to_response(
                self.get_context_data(form=timesheet_form,
                    project_form=timesheet_entry_formset))

    def post(self, request, *args, **kwargs):
        try:
            self.timesheet = ProjectTS.objects.get(
                    pay_period_begin__lte=timezone.now(),
                    pay_period_end__gte=timezone.now(),
                    ambassador=self.request.user)
        except ProjectTS.DoesNotExist:
            self.timesheet = None

        self.object = None
        form = ProjectTSModelForm(self.request.POST, instance=self.timesheet)

        project_form = ProjectFormSet(self.request.POST, request.FILES, instance=self.timesheet)
        if (form.is_valid() and project_form.is_valid()):
            return self.form_valid(form, project_form)
        else:
            return self.form_invalid(form, project_form)

    def form_valid(self, form, project_form):
        self.object = form.save(commit=False)
        self.object.ambassador = self.request.user
        self.object.save()
        project_form.instance = self.object
        project_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, project_form):
        print("invalidates once")
        print(form.errors)
        return self.render_to_response(
            self.get_context_data(form=form,
                                  project_form=project_form))


def ProjectTSApprovalView(request):

    ProjectTSEntryApprovalFormSet = modelformset_factory(ProjectTSEntry,
            form=ProjectTSEntryApprovalForm,
            extra=0)
    entries = ProjectTSEntry.objects.filter(project_leader=request.user,
            project_leader_verification=False).order_by('project_time_sheet__ambassador')

    if request.method == 'GET':
        formset = ProjectTSEntryApprovalFormSet(queryset=entries)
        return render_to_response('project_approval_list.html',
                {'form': formset},
                context_instance=RequestContext(request),)

    else:
        formset = ProjectTSEntryApprovalFormSet(request.POST or None, queryset=entries)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect('/profile/')
