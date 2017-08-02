# Django
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.db import transaction
from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import generic

# Local Django
from asiapp.mixins import LoginRequiredMixin
from .forms import UpdateOrCreateHourLimitForm
from .models import TimeRestriction

class UpdateOrCreateHourLimitView(LoginRequiredMixin, generic.UpdateView):
    model = TimeRestriction
    form_class = UpdateOrCreateHourLimitForm
    template_name = 'update_or_create_form.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        obj, created = TimeRestriction.objects.get_or_create(
                user=self.request.user,
                defaults={'user': self.request.user},
        )
        return obj
