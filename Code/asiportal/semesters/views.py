from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.db import transaction
from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import generic
from asiapp.mixins import LoginRequiredMixin
from django.shortcuts import render

from .models import AmbassadorSurvey, TuteeSurvey
from .forms import AmbassadorSurveyForm, TuteeSurveyForm

# Create your views here.

#This view will be for choosing which survey list to view, Group or Individual
class GeneralSurveyView(LoginRequiredMixin, generic.TemplateView):
    template_name = "general_survey.html"

#View to fill form out for individual surveys for Ambassadors
class AmbassadorSurveyView(generic.FormView):
    form_class = AmbassadorSurveyForm
    template_name = 'surveys/ambassador_survey.html'
    model = AmbassadorSurvey
    success = reverse_lazy('surveys:surveys:success_survey')

    def form_valid(self, form):
        self.object = form.save(commit=False)
            #tutee absent, mark their survey as done
        if self.object.tutee_absent:
            pass
            #session canceled mark tutee survey as done
        if self.object.session_canceled:
            pass
        self.object.save()
        return super(AmbassadorSurveyView, self).form_valid(form)

#Lists surveys for Ambassadors to do for individual sessions
class AmbassadorListSurveys(LoginRequiredMixin, generic.ListView):
    template_name = 'surveys/ambassador_survey_list.html'

#View to fill form out for individual surveys for Tutees
class TuteeSurveyView(generic.FormView):
    form_class = TuteeSurveyForm
    template_name = 'surveys/tutee_survey.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return super(TuteeSurveyView, self).form_valid(form)

#Lists surveys for Ambassadors to do for individual sessions
class TuteeListSurveys(LoginRequiredMixin, generic.ListView):
    pass

