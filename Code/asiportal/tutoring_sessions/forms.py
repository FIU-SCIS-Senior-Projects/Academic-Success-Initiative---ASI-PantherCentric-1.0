from django import forms
from functools import partial
from django.contrib.auth.models import User
from tutoring_sessions.models import Session
DateInput = partial(forms.DateInput, {'class': 'datepicker'})

class TutoringSessionUpdateForm(forms.ModelForm):

    class Meta:
        model = Session
        fields = [] 
    ambassador = forms.ModelChoiceField(queryset=User.objects.all())
    start_date = forms.DateField()

    def __init__(self, *args, **kwargs):
        super(TutoringSessionUpdateForm, self).__init__(*args, **kwargs)
        self.fields['ambassador'].label_from_instance = lambda x : x.get_full_name()
        self.fields['ambassador'].label = 'New Ambassador'
        self.fields['start_date'].label = 'New Session Start Date'
        self.fields['start_date'].help_text = '<br>NOTE: Dates must be in the format YYYY-MM-DD'

class TimeSheetForm(forms.Form):
    start_date = forms.DateField(widget=DateInput())
    end_date = forms.DateField(widget=DateInput())
    team_leader = forms.ModelChoiceField(queryset=User.objects.filter(groups__name='Team Leader'))

    def __init__(self, *args, **kwargs):
        super(TimeSheetForm, self).__init__(*args, **kwargs)
        self.fields['team_leader'].label_from_instance = lambda x : x.get_full_name()
