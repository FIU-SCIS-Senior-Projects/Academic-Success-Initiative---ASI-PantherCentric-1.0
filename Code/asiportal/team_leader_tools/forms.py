from django import forms

from . import models

#   Form can create course to add times to
#       only show courses for that team leader
#
class PollGeneratorListCreateForm(forms.ModelForm):
    class Meta:
        model = models.PollTime
        fields =  [
                    'time_start',
                    'time_end',
                    'day',
        ]

PollGeneratorFormSet = forms.modelformset_factory(
    models.PollTime,
    form=PollGeneratorListCreateForm,
    min_num=1,
    can_delete=True,
    )
