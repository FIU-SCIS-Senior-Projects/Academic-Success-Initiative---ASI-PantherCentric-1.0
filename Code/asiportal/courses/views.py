from django.http import HttpResponseRedirect
from django.utils import timezone
from django.shortcuts import render
from django.views import generic
from asiapp.mixins import LoginRequiredMixin
from semesters.models import Semester
from .models import Course

IN_A = ['STA3033', 'MAD2104', 'MAC2312', 'MAC2311', 'MAC1140', 'MAC1114', 'MAC1105']
IN_B = ['COP4338', 'COT3100', 'MAC1105', 'MAC1114', 'MAC1140', 'MAC1147', 'MAC2311', 'MAC2312', 'MAD1100', 'MAD3512', ]
IN_C = ['CDA3103', 'COP2210', 'COP2250', 'COP3337', 'COP3530', 'COP3804', 'COP4338', 'COP4814', 'COT3100', 'MAC1114', 'MAC1140', 'MAC1147', 'MAC2311', 'MAC2312', 'MAD2104', ]

class CourseListView(LoginRequiredMixin, generic.ListView):
    model = Course

    def get_context_data(self, **kwargs):
        context = super(CourseListView, self).get_context_data(**kwargs)
        context['semesters'] = Semester.objects.current()
        if Semester.objects.current()[0].term in ['SA', 'SB', 'SC']:
            context['is_summer'] = True
            context['summer_a'] = Semester.objects.get(term='SA', year=timezone.now().year)
            context['in_a'] = Course.objects.filter(name__in=IN_A)
            context['in_b'] = Course.objects.filter(name__in=IN_B) 
            context['summer_b'] = Semester.objects.get(term='SB', year=timezone.now().year)
            context['in_c'] = Course.objects.filter(name__in=IN_C)
            context['summer_c'] = Semester.objects.get(term='SC', year=timezone.now().year)
        else:
            context['is_summer'] = False
            context['in_a'] = []
            context['in_b'] = []
            context['in_c'] = []
            context['summer_a'] = False
            context['summer_b'] = False
            context['summer_c'] = False
        return context

    def get_queryset(self):
        queryset = super(CourseListView, self).get_queryset()
        queryset = queryset.exclude(team = None).order_by('name')
        return queryset
