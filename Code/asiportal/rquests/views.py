from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.utils import timezone
from django.views import generic
from asiapp.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from courses.models import Course
from .models import (
        TutoringRequest,
        SessionCancelationRequest,
        )
from .forms import (
        RequestTutoringForm,
        UpdateTutoringRequestForm,
        TutoringRequestCreateForm,
        SessionCancelationRequestCreateForm,
        SessionCancelationRequestUpdateForm,
        )
from tutoring_sessions.models import Session, IndividualSession
from rquests.services.ticket_updates import update_other_times
from rquests.services.gcal_inviter import send_invite
from rquests.services.emailer import (
        tutoring_confirmation_email,
        request_submission_email,
        no_room_available_email,
        )
from surveys.models import AmbassadorSurvey, TuteeSurvey

'''
Django is a python framework which follows the Model View Controller 
design pattern. However in Django the names are slighlty different
: 

Model ( Model )
Template ( View )
View ( Controller )

The view might be the most important part of the app since it is the 
interface between the user and the database ( the good stuff )

So in order to facilitate ease of implemntation Django has two main ways of 
writing Views. They are function based views and class based views.

Function based views allow for the most freedom as you are responsible for 
defining every single bit of action that occurs.

Class based views have most of the predefined behavior you will most likely need in a view,
so they allow to easily and quickly create the functionality you need with the least amount of 
code.
In this project class based views are used almost exclusively for that reason. If you'd like to
see some documentation for all the class based views and all their methods, please check out
http://ccbv.co.uk
It might be the best documentation ( and potentially only documentation outside of the source code ) 
you'll find on class based views. 

In general, we have a view for the basic CRUD 
( CREATE READ UPDATE DELETE) Operations.
They are ( respectively )
CreateView ( or FormView depending )
DetailView ( I guess a ListView might count )
UpdateView
DeleteView

There is also a TemplateView but that is more so for serving static HTML pages.
These are the main class based views you will find throughout this project
'''

'''
This is a simple TemplateView
All it does is returns some template with more or less static content.
It is not responsible for anything other than retrieving an html file and returning 
it to the user.
'''
class RequestDirectoryView(generic.TemplateView):
    template_name = 'rquests/directory.html'

    '''
    The dispatch(...) method is typically overwritten if we want
    to ensure that only certain users can access a page
    '''
    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm('rquests.change_tutoringrequest'):
            return super(RequestDirectoryView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')

'''
This is a FormView
This returns a HTML page with a form to allow some kind of change to happen 
in the database.
'''
class RequestTutoringFormView(LoginRequiredMixin, generic.FormView):
    form_class = RequestTutoringForm
    template_name = 'rquests/request_tutoring_form.html'
    success_url = reverse_lazy('requests:request_success')

    '''
    Once again, dispatch for authnetication purposes. Here we make sure the user is logged in.
    '''
    def dispatch(self, request, *args, **kwargs):
        # if the user is logged in give them the regular dispatch function
        if request.user.is_authenticated():
            return super(RequestTutoringFormView, self).dispatch(request, *args, **kwargs)
        # otherwise redirect them to the login screen
        else:
            return HttpResponseRedirect('/')

    '''
    For this particular view, we use the URL parameters to determine what course and 
    semeseter the user is registering for. So we update the dictionary kwargs with
    the key course and value of url keyword course. The same is done for the semester
    '''
    def get_form_kwargs(self):
        kwargs = super(RequestTutoringFormView, self).get_form_kwargs()
        kwargs['course'] = self.kwargs['course']
        kwargs['semester'] = self.kwargs['semester']
        return kwargs

    '''
    This is function which is responsible for generating the context dictionary that will
    be used in the template.
    '''
    def get_context_data(self, *args, **kwargs):
        cd = super(RequestTutoringFormView, self).get_context_data(*args, **kwargs)
        # check how many pending requests the user has
        open_requests = self.request.user.tutoring_requests.filter(status='A').count()
        # check how many sessions that havent ended the user has
        scheduled_sessions = self.request.user.sessions.filter(end_date__gte=timezone.now()).count()
        total_sessions = open_requests + scheduled_sessions
        # check if the user has surpsased the limit of scheduled sessions allowed
        if total_sessions > 4:
            cd['has_too_many_sessions'] = True
        else:
            cd['has_too_many_sessions'] = False
        return cd

    '''
    This is the function which gets called when the form.is_valid() returns true
    '''
    def form_valid(self, form):
        # create the "object" of the model
        request = form.save(commit=False)
        # fill in the rest of the required model details
        # check if we are in summer. if we are we need to check
        # if there is a corresponding availability in
        # B, C, or A that needs to be updated
        if request.availability.semester.is_summer():
            potential = request.availability.find_related_summer()
            for av in potential:
                av.is_scheduled = True
                av.save()
        request.submitted_by = self.request.user
        request.course = Course.objects.get(slug=self.kwargs['course'])
        # commit the changes and create the model in the databaese
        request.save()
        # send an email with the request info
        request_submission_email(request)
        return super(RequestTutoringFormView, self).form_valid(form)

class RequestSuccessView(generic.TemplateView):
    template_name = 'rquests/request_success.html'

'''
This is an UpdateView.
This takes an existing Model and makes some kind of change to it.
'''
class UpdateTutoringRequestFormView(LoginRequiredMixin, 
                                    generic.UpdateView):
    template_name = 'rquests/update_tutoring_request_form.html'
    form_class = UpdateTutoringRequestForm
    queryset = TutoringRequest.objects.all()
    success_url = '/'

    # Not much is different from the other views
    def dispatch(self, request, *args, **kwargs):
        # .has_perm can check if a certain perkmission exists
        if request.user.has_perm('rquests.change_tutoringrequest'):
            return super(UpdateTutoringRequestFormView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')

    # same as the other form_valid method
    def form_valid(self, form):
        ## missing a situation where the session is cancled..
        if form.cleaned_data['status'] == 'B':
            sessions = Session().create_from_form(form)
            tutoring_confirmation_email(sessions[0].session)
            # dont use this in production for now
            #send_invite(sessions[0].session)
            AmbassadorSurvey.create_surveys_from_individual_sessions(sessions)
            TuteeSurvey.create_surveys_from_individual_sessions(sessions)
        elif form.cleaned_data['status'] == 'D':
            temp = form.save(commit=False)
            no_room_available_email(temp)
            update_other_times(temp.availability)
            form.save()
        else:
            form.save(commit=False)
        return super(UpdateTutoringRequestFormView, self).form_valid(form)

'''
This is a ListView
It gets a query of models and returns that queryset for use 
in a template.
'''
class TutoringRequestListView(generic.ListView):
    model = TutoringRequest

    '''
    The method which gets your "Queryset" ( a python list of models )
    from the database. The ORM in DJango is pretty intuitve and easy to use ( compared to raw SQL)
    '''
    def get_queryset(self):
        # if the ordered kwarg is present in URL 
        if 'order' in self.kwargs:
            qs = TutoringRequest.objects.filter(status=self.kwargs['order']).order_by('submitted_at')
        else:
            qs = TutoringRequest.objects.all().order_by('status', 'submitted_at')
        return qs.filter(availability__semester__end_date__gte=timezone.now())

    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm('rquests.change_tutoringrequest'):
            return super(TutoringRequestListView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')

'''
Slightly different than the FormView although this also needs a form.
The formView renders a form and a response
The createview renders a form and creates a new record in the db.
'''
class TutoringRequestCreateView(generic.CreateView):
    model = TutoringRequest
    form_class = TutoringRequestCreateForm
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm('team_leader_tools.change_polltime'):
            return super(TutoringRequestCreateView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')

    def get_form_kwargs(self):
        kwargs = super(TutoringRequestCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class SessionCancelationRequestCreateView(generic.CreateView):
    model = SessionCancelationRequest
    form_class = SessionCancelationRequestCreateForm
    
    def dispatch(self, request, *args, **kwargs):
        # needs a different permission
        # for ambassadors as well
        if request.user.has_perm('rquests.add_sessioncancelationrequest'):
            return super(SessionCancelationRequestCreateView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super(SessionCancelationRequestCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class SessionCancelationRequestListView(generic.ListView):
    model = SessionCancelationRequest

    def get_queryset(self):
        qs = SessionCancelationRequest.objects.filter(session__end_date__gte=timezone.now())
        return qs.order_by('status')
    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm('rquests.change_tutoringrequest'):
            return super(SessionCancelationRequestListView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')

class SessionCancelationRequestUpdateView(generic.UpdateView):
    model = SessionCancelationRequest
    form_class= SessionCancelationRequestUpdateForm
    template_name = 'rquests/sessioncancelation_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm('rquests.change_tutoringrequest'):
            return super(SessionCancelationRequestUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')
    success_url = reverse_lazy('requests:session_cancelation_requests')

    def form_valid(self, form):
        request = form.save(commit=False)
        sess = request.session
        sess.availability.is_scheduled = False
        # when a summer C session gets canceled 
        # go through and update any and all summer B and A availabilities
        if sess.availability.semester.term == 'SC':
            to_update = sess.availability.find_related_summer()
            for av in to_update:
                av.is_scheduled = False
                av.save()
        sess.availability.save()
        sess.end_date = request.submitted_at
        sess.save()
        IndividualSession.remove_after_date(sess, sess.end_date)
        return super(SessionCancelationRequestUpdateView, self).form_valid(form)
