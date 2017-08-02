# Django
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.db import transaction
from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.shortcuts import render
from django.utils import timezone
from django.db.models import F

# local Django
from asiapp.mixins import LoginRequiredMixin
from .models import AmbassadorSurvey, TuteeSurvey
from .forms import AmbassadorSurveyForm, TuteeSurveyForm
from tutoring_sessions.models import Session


#View to fill form out for individual surveys for Ambassadors
class AmbassadorSurveyView(LoginRequiredMixin, generic.UpdateView):
    form_class = AmbassadorSurveyForm
    template_name = 'ambassador_survey.html'
    model = AmbassadorSurvey
    success_url = reverse_lazy('surveys:success_survey')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.submitted = True
        self.object.submitted_on = timezone.now()

        #if tutee absent mark submitted and tutee absent as True
        if self.object.tutee_absent:
            tutee_surv = get_object_or_404(
                    TuteeSurvey,
                    individual_session=self.object.individual_session)
            tutee_surv.tutee_absent = True
            tutee_surv.submitted = True
            tutee_surv.save()

        #if tutee session canceled submitted and session canceled as True
        if self.object.session_canceled:
            tutee_surv = get_object_or_404(
                    TuteeSurvey,
                    individual_session=self.object.individual_session)
            tutee_surv.session_canceled = True
            tutee_surv.submitted = True
            tutee_surv.save()

        self.object.save()
        return super(AmbassadorSurveyView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AmbassadorSurveyView, self).get_context_data(**kwargs)
        context['tutee_name'] = \
            self.object.individual_session.session.tutee.get_full_name
        return context


#Lists surveys for Ambassadors to do for individual sessions
class AmbassadorListSurveysView(LoginRequiredMixin, generic.ListView):
    template_name = 'ambassador_survey_list.html'
    model = AmbassadorSurvey

    def get_queryset(self):
        querySet = AmbassadorSurvey.objects.filter(
                individual_session__session__availability__ambassador = \
                    self.request.user,
                individual_session__session_date__lte=timezone.now(),
                submitted=False,
                )
        return querySet

#View to fill form out for individual surveys for Tutees
class TuteeSurveyView(generic.UpdateView):
    form_class = TuteeSurveyForm
    template_name = 'tutee_survey.html'
    model = TuteeSurvey
    success_url = reverse_lazy('surveys:success_survey')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.submitted = True
        self.object.submitted_on = timezone.now()
        self.object.save()
        return super(TuteeSurveyView, self).form_valid(form)

#Lists surveys for Ambassadors to do for individual sessions
class TuteeListSurveysView(LoginRequiredMixin, generic.ListView):
    template_name = 'tutee_survey_list.html'

    def get_queryset(self):
        querySet = TuteeSurvey.objects.filter(
                individual_session__session__tutee=self.request.user,
                individual_session__session_date__lte=timezone.now(),
                submitted=False
                )
        return querySet

class TuteeListCourseSurveysView(LoginRequiredMixin, generic.ListView):
    template_name = 'tutee_survey_list.html'

    def dispatch(self, request, *args, **kwargs):
        session = get_object_or_404(Session, pk=self.kwargs['session_pk'])
        if request.user != session.tutee:
            return HttpResponseRedirect(reverse_lazy('home'))
        else:
            return super(TuteeListCourseSurveysView, self)\
                        .dispatch(request, *args, **kwargs)

    def get_queryset(self):
        querySet = TuteeSurvey.objects.filter(
                individual_session__session__tutee=self.request.user,
                individual_session__session_date__lte=timezone.now(),
                submitted=False,
                individual_session__session__pk=self.kwargs['session_pk'],
                )
        return querySet

class AmbassadorListCourseSurveysView(LoginRequiredMixin, generic.ListView):
    template_name = 'ambassador_survey_list.html'

    def dispatch(self, request, *args, **kwargs):
        session = get_object_or_404(Session, pk=self.kwargs['session_pk'])
        if request.user != session.availability.ambassador:
            return HttpResponseRedirect(reverse_lazy('home'))
        else:
            return super(AmbassadorListCourseSurveysView, self)\
                        .dispatch(request, *args, **kwargs)

    def get_queryset(self):
        querySet = AmbassadorSurvey.objects.filter(
            individual_session__session__availability__ambassador = \
                self.request.user,
            individual_session__session_date__lte=timezone.now(),
            submitted = False,
            individual_session__session__pk=self.kwargs['session_pk'],
                ).distinct()
        return querySet

class SuccessView(LoginRequiredMixin, generic.TemplateView):
    template_name = "success.html"

class SurveyStatusListView(LoginRequiredMixin, generic.ListView):
    '''
    ListView to return the incompleted surveys of an ambassadors tutee
    '''

    template_name = "survey_status_list.html"

    def dispatch(self, request, *args, **kwargs):
        session = get_object_or_404(Session, pk=self.kwargs['session_pk'])
        if request.user != session.availability.ambassador:
            return HttpResponseRedirect(reverse_lazy('home'))
        else:
            return super(SurveyStatusListView, self)\
                        .dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = TuteeSurvey.objects.filter(
            individual_session__session__availability__ambassador = \
                self.request.user,
            individual_session__session_date__lte=timezone.now(),
            individual_session__session__pk=self.kwargs['session_pk'],
            submitted = False
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super(SurveyStatusListView, self).get_context_data(**kwargs)
        context['tutee_name'] = \
            Session.objects.get(
                    pk = self.kwargs['session_pk']
            ).tutee.get_full_name
        return context
