from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.db import transaction
from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views import generic
from .models import Availability
from asiapp.mixins import LoginRequiredMixin
from .forms import SubmitAvailabilityForm, AvailabilityUpdateForm

class SubmitAvailabilityFormView(generic.FormView):
    form_class = SubmitAvailabilityForm
    template_name = 'availabilities/submit_form.html'
    success_url = reverse_lazy('availabilities:list')

    def form_valid(self, form):
        try:
            if form._times:
                Availability.create_with_times(self.request.user, form)
            else:
                Availability.create_from_form(self.request.user, form)
            return super(SubmitAvailabilityFormView, self).form_valid(form)

        except IntegrityError:
            form.add_error('start_time','This time already exists')
            form.add_error('end_time','This time already exists')
            form.add_error('day','This time already exists')
            return render(self.request, self.template_name, {'form' : form})

class AvailabilityListView(LoginRequiredMixin
            ,generic.ListView):
    model = Availability
    def get_queryset(self):
        qs = Availability.objects.filter(ambassador=self.request.user,
               semester__end_date__gte=timezone.now() )
        return qs

class AvailabilityUpdateView(generic.UpdateView):
    model = Availability
    form_class = AvailabilityUpdateForm
    template_name = 'availabilities/update_form.html'
    success_url = reverse_lazy('availabilities:list')

    def form_valid(self, form):
        try:
            if form._times:
                Availability.create_with_times(self.request.user, form)
            else:
                Availability.create_from_form(self.request.user, form)
            return super(AvailabilityUpdateView, self).form_valid(form)

        except IntegrityError:
            form.add_error('start_time','This time already exists')
            form.add_error('end_time','This time already exists')
            form.add_error('day','This time already exists')
            return render(self.request, self.template_name, {'form' : form})

class AvailabilityDeleteView(generic.DeleteView):
    model = Availability
    template_name = 'availabilities/confirm_delete.html'
    success_url = reverse_lazy('availabilities:list')
