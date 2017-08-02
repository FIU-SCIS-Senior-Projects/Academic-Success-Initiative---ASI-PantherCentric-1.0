from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views import generic
from .forms import CreateAltUserForm
from .models import Videos, AltUser
from .services import services

# reference
class TestView(generic.TemplateView):
    template_name = 'atrisk/test.html'

class LandingView(generic.TemplateView):
    template_name = 'atrisk/landing.html'

    def get_context_data(self, **kwargs):
        cd = super(LandingView, self).get_context_data(**kwargs)
        cd['is_advisor'] = self.request.user.has_perm('add_altuser')
        return cd


class VideoView(generic.DetailView):
    template_name = 'atrisk/watch_video.html'
    model = Videos
    slug_field = 'url_code'
    slug_url_kwarg = 'urlcode'

    def get_context_data(self, **kwargs):
       cd = super(VideoView, self).get_context_data(**kwargs)
       if services.is_atrisk(self.request.user):
        cd['altuser'] = get_object_or_404(AltUser, username=self.request.user)
       else:
        cd['altuser'] = self.request.user
       return cd
        

class StudentVideoListView(generic.ListView):
    model = Videos
    template_name = 'atrisk/video_listview.html'

class AdvisorVideoListView(generic.ListView):
    model = Videos
    template_name = 'atrisk/a_video_listview.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm('add_altuser'):
            return super(AdvisorVideoListView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse_lazy('home'))

class SuccessView(generic.TemplateView):
    template_name = 'atrisk/success.html'

class StudentAccountCreationView(generic.CreateView):
    model = AltUser
    template_name = 'atrisk/studentacct_createview.html'
    form_class = CreateAltUserForm
    success_url = reverse_lazy('atrisk:success')

    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm('add_altuser'):
            return super(StudentAccountCreationView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse_lazy('home'))

class ViewCountView(generic.TemplateView):
    template_name = 'atrisk/viewcount.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm('add_altuser'):
            return super(ViewCountView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse_lazy('home'))

    def get_context_data(self, **kwargs):
        urlcode = kwargs.pop('urlcode')
        title = Videos.objects.get(url_code=urlcode).title
        cd = super(ViewCountView, self).get_context_data(**kwargs)
        cd['mixpanel'] = services.get_stats(title)
        cd['video_title'] = title
        return cd
