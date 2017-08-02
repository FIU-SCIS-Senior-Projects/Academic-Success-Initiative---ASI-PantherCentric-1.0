from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, Http404
from asiapp.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic
from .models import UserProfile
from .forms import UserProfileCreateForm
from django.core.urlresolvers import reverse_lazy

class UserProfileCreateView(LoginRequiredMixin, generic.CreateView):
    model = UserProfile
    form_class = UserProfileCreateForm
    template_name = 'user_profiles/user_profile_create.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super(UserProfileCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('user_profiles:detail', kwargs={
            'pk' : self.request.user.pk
            })

class UserProfileDetailView(LoginRequiredMixin, generic.DetailView):
    model = UserProfile
    template_name = 'user_profiles/user_profile_detail.html'

    def get_object(self, queryset=None):
        try:
            obj = self.request.user.profile
            return obj
        except ObjectDoesNotExist:
            return None

class UserProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = UserProfile
    form_class = UserProfileCreateForm
    template_name = 'user_profiles/user_profile_update.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object is None:
            return HttpResponseRedirect(reverse_lazy('user_profiles:create'))
        else:
            return super(UserProfileUpdateView, self).get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        obj = super(UserProfileUpdateView, self).get_object(queryset=None)
        if obj.user is not self.request.user:
            try:
                return self.request.user.profile
            except ObjectDoesNotExist:
                return None
        else:
            return obj

    def get_success_url(self):
        return reverse_lazy('user_profiles:detail', kwargs={
            'pk' : self.request.user.pk
            })
