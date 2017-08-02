# Django
from django.forms import ModelForm
from django import forms

# Local Django
from . import models

class UpdateOrCreateHourLimitForm(ModelForm):
    class Meta:
        model = models.TimeRestriction
        fields = [
            'max_time',
        ]

    def __init__(self, *args, **kwargs):
        super(UpdateOrCreateHourLimitForm, self).__init__(*args, **kwargs)
        self.fields['max_time'] = forms.IntegerField(max_value=10, min_value=1)
