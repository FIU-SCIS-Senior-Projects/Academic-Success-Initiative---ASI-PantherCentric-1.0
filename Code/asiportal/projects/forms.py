from datetime import timedelta
from django import forms
from django.utils import timezone
from django.forms import BaseModelFormSet, ModelForm, modelformset_factory, widgets
from django.forms.models import inlineformset_factory
from functools import partial
from .models import ProjectTSEntry, ProjectTS

DateInput = partial(forms.DateInput, {'class': 'datepicker'})

class ShowNameChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()

class ProjectTSModelForm(ModelForm):
    class Meta:
        model = ProjectTS
        fields = ('pay_period_begin', 'pay_period_end')
    pay_period_begin = forms.DateField(widget=DateInput())
    pay_period_end = forms.DateField(widget=DateInput())

ProjectFormSet = inlineformset_factory(ProjectTS,
                    ProjectTSEntry,
                    fields=('description',
                        'project_leader',
                        'project_time_sheet',
                        'title',
                        'start_time',
                        'end_time',
                        'day',
                    ),
                    field_classes = {
                        'project_leader' : ShowNameChoiceField,
                        },
                    widgets={
                        'start_time' : widgets.TimeInput(format='%I:%M'),
                        'end_time' : widgets.TimeInput(format='%I:%M'),
                        'day' : DateInput()
                    },
                    extra=1,
                    can_delete=True
                    )

class ProjectTSApprovalForm(ModelForm):
    class Meta:
        model = ProjectTS
        fields = ('ambassador_finalized',)

ProjectApprovalFormSet = inlineformset_factory(ProjectTS,
                    ProjectTSEntry,
                    fields=('description',
                        'project_leader_verification',
                        'project_leader',
                        'title',
                        'start_time',
                        'end_time',
                        'day',
                    ),
                    )

class ProjectTSEntryApprovalForm(ModelForm):
    project_leader_verification = forms.BooleanField(required=False)
    description = forms.CharField(required=False)
    title = forms.CharField(required=False)
    start_time = forms.TimeField(required=False)
    total_time = forms.IntegerField(required=False)
    end_time = forms.TimeField(required=False)
    day = forms.DateField(required=False)

    class Meta:
        model = ProjectTSEntry
        exclude = ['project_time_sheet', 'project_leader']


