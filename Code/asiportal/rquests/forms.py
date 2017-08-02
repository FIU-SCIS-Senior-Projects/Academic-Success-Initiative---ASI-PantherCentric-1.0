from django import forms
from django.utils import timezone
from availabilities.models import Availability
from courses.models import Course
from tutoring_sessions.models import Session, ROOMS
from rquests.models import (
        TutoringRequest,
        SessionCancelationRequest,
        )
from restrictions.models import TimeRestriction


class RequestTutoringForm(forms.ModelForm):
    class Meta:
        model = TutoringRequest
        fields = ('availability',)

    def __init__(self, *args, **kwargs):
        semester = kwargs.pop('semester')
        self.semester = semester.replace('-', ' ').title()
        course_name = kwargs.pop('course')
        self.course = Course.objects.get(slug=course_name)
        super(RequestTutoringForm, self).__init__(*args,**kwargs)
        over = TimeRestriction.objects.overtime()
        _all = Availability.objects.prefetch_related('ambassador', 'semester').filter(is_scheduled=False)
        self.fields['availability'].queryset = _all.filter(ambassador__courses=self.course, semester__slug=semester).exclude(ambassador__in = over)

class UpdateTutoringRequestForm(forms.ModelForm):
    class Meta:
        model = TutoringRequest
        fields = ('status',)
    room_number = forms.ChoiceField(choices=ROOMS, initial='101A')

class TutoringRequestCreateForm(forms.ModelForm):
    class Meta:
        model = TutoringRequest
        exclude = ['status', 'submitted_at', 'updated_at']
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(TutoringRequestCreateForm, self).__init__(*args, **kwargs)
        courses = user.teams.all()
        self.fields['course'].queryset = courses
        teams = list()
        for c in courses:
            [teams.append(member.pk) for member in c.team.all()]
        self.fields['submitted_by'].label = 'Tutee'
        self.fields['submitted_by'].label_from_instance = lambda x : x.get_full_name()
        self.fields['availability'].queryset = Availability.objects.filter(
                ambassador__pk__in = teams,
                is_scheduled = False,
                )

class SessionCancelationRequestCreateForm(forms.ModelForm):
    class Meta:
        model = SessionCancelationRequest
        fields = ['session', 'reason']
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(SessionCancelationRequestCreateForm, self).__init__(*args, **kwargs)
        self.fields['session'].queryset = Session.objects.filter(
                availability__ambassador = user)

class SessionCancelationRequestUpdateForm(forms.ModelForm):
    class Meta:
        model = SessionCancelationRequest
        fields = ['status']
