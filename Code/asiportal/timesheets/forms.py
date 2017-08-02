from surveys.models import AmbassadorSurvey, TuteeSurvey
from datetime import timedelta
from django import forms
from django.utils import timezone
from functools import partial
from tutoring_sessions.models import IndividualSession
from .models import TimeSheet, TutoringTimeSheetEntry

DateInput = partial(forms.DateInput, {'class': 'datepicker'})

# THIS THING IS SLOW !!!
# JUST TRYNA FIND A BETTER WAY!!!!!!!
ALL_SURVS_AMB = AmbassadorSurvey.objects.all()
ALL_SURVS_TUT = TuteeSurvey.objects.all()

class FinalApproveTimeSheetForm(forms.ModelForm):
    class Meta:
        model = TimeSheet
        exclude = ['__all__',]

class TimeSheetForm(forms.ModelForm):
    class Meta:
        model = TimeSheet
        fields = ['pay_period_begin', 'pay_period_end']
    pay_period_begin = forms.DateField(widget=DateInput())
    pay_period_end = forms.DateField(widget=DateInput())

'''

              __[]__ 
           ,-`---.--`;.         (} - lmao dude what were you thinking
      .---' '---'.-.-- '----.  </\ 
     /   .-.    {K9}     .-. \  |\'-._
     '--(( ))-----------(( ))' /  |   `',___/> - i know right, this shit is ASS
  jgs    `"`             `"`   `  `     /> >\
          oh fuck its the bad code police
          DIS SHIT IS HELLLLLA SLOW
'''
class TutoringTimeSheetEntryApprovalForm(forms.ModelForm):
    class Meta:
        model = TutoringTimeSheetEntry
        fields = ['tl_verified']

    session = forms.CharField(widget = forms.Textarea(attrs={'style' : 'max-height : 75px'}) , disabled=True, )
    hours = forms.IntegerField(disabled=True)

    def __init__(self, *args, **kwargs):
        super(TutoringTimeSheetEntryApprovalForm, self).__init__(*args, **kwargs)
        if self.instance.id:
            # this looks bad
            _amb = ALL_SURVS_AMB.get(
                    individual_session=self.instance.session)
            # this looks bad
            _tut = ALL_SURVS_TUT.get(
                    individual_session=self.instance.session)
            self.ent_id = self.instance.id
            self.amb_complete = _amb.submitted
            self.tut_complete = _tut.submitted
            self.comments = _amb.comments
            self.session_canceled = _amb.session_canceled
            self.tut_absent = _amb.tutee_absent
            self.fields['session'].initial = self.instance.session
            self.fields['hours'].initial = self.instance.total_time


class TutoringTimeSheetEntryForm(forms.ModelForm):
    class Meta:
        model = TutoringTimeSheetEntry
        fields = ['session', 'total_time']
    pk_field = None
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self._parent = kwargs.pop('parent')
        base = self._parent.pay_period_begin
        end = self._parent.pay_period_end
        super(TutoringTimeSheetEntryForm, self).__init__(*args, **kwargs)
        _all = IndividualSession.objects.prefetch_related('session', 'session__course', 'session__ambassador', 'session__tutee').all()
        _ex = TutoringTimeSheetEntry.objects.filter(timesheet=self._parent)
        _exclude = [entry.session.id for entry in _ex]
        self.fields['session'].queryset = _all.filter(
                session__ambassador = self.user,
                session_date__range=[base, end],
                ).exclude(id__in = _exclude)

TimeSheetEntryFormSet = forms.formset_factory(
        TutoringTimeSheetEntryForm,
        extra = 1,
        min_num = 0,
        can_delete = True,
        )

TimeSheetEntryApprovalFormSet = forms.modelformset_factory(
        TutoringTimeSheetEntry,
        extra = 0,
        form=TutoringTimeSheetEntryApprovalForm,
        )
