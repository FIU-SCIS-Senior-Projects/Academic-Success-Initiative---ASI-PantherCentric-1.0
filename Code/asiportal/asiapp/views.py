from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import generic
from .services.account_emailer import send_account_confirmation_link
from .forms import (
        LogInForm,
        CreateAccountForm,
        ForgotPasswordForm,
        ActivateAccountForm,
        )
from tokens.models import AccountActivationToken

class ActivateAccountView(generic.UpdateView):
    model = AccountActivationToken
    form_class = ActivateAccountForm
    success_url = reverse_lazy('login')
    template_name = 'activate_account.html'

    def get_object(self, queryset=None):
        obj = get_object_or_404(AccountActivationToken,
                token=self.kwargs['token'])
        return obj

    def form_valid(self, form):
        token = form.save(commit=False)
        if not token.used:
            user = token.user
            user.is_active = True
            user.save()
            token.used = True
            token.save()
            return super(ActivateAccountView, self).form_valid(form)
        else:
            return HttpResponseRedirect(reverse_lazy('home'))


class HomePageView(generic.TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        cd = super(HomePageView, self).get_context_data(**kwargs)
        cd['is_advisor'] = self.request.user.has_perm('atrisk.add_altuser')
        cd['is_project_lead'] = self.request.user.has_perm('timesheets.approve_timesheet')
        return cd

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return super(HomePageView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse_lazy('login'))

class AccountSuccessTemplateView(generic.TemplateView):
    template_name = 'account_success.html'

class LoginView(generic.FormView):
    template_name = 'login.html'
    form_class = LogInForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(self.request, user)
            return super(LoginView, self).form_valid(form)
        else:
            return self.form_invalid(form)

class CreateAccountFormView(generic.CreateView):
    model = User
    form_class = CreateAccountForm
    template_name = 'create_account_form.html'
    success_url = reverse_lazy('account_success')

    def form_valid(self, form):
        user = form.save()
        tok = AccountActivationToken.objects.create(user=user)
        send_account_confirmation_link(user, tok)
        return HttpResponseRedirect(self.success_url)

def log_out(request):
  if request.user.is_authenticated():
    logout(request)
  return HttpResponseRedirect(reverse_lazy('home'))

class ProfileDirectoryView(generic.TemplateView):
    template_name = 'profile_directory.html'
    def get_context_data(self, **kwargs):
        context_data = super(ProfileDirectoryView, self).get_context_data(**kwargs)
        context_data['can_have_availability'] = self.request.user.has_perm('availabilities.add_availability')
        context_data['can_cancel_sessions'] = self.request.user.has_perm('rquests.add_sessioncancelationrequest')
        context_data['can_add_time_restriction'] = self.request.user.has_perm('restrictions.add_timerestriction')
        return context_data

class ForgotPasswordView(generic.FormView):
    form_class = ForgotPasswordForm
