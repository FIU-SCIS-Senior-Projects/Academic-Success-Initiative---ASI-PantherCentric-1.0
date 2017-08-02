from datetime import time
from .models import Availability
from semesters.models import Semester
from django import forms
from django.utils import timezone

ACCEPTED_FORMATS = ('%H:%M:%S',
                    '%I:%M %p',
                    '%I:%M%p',
                    )

class SubmitAvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ['start_time', 'end_time', 'day', 'semester']

    start_time = forms.TimeField(input_formats=ACCEPTED_FORMATS)
    end_time = forms.TimeField(input_formats=ACCEPTED_FORMATS)
    _times = list()

    def __init__(self, *args, **kwargs):
        super(SubmitAvailabilityForm, self).__init__(*args, **kwargs)
        self.fields['semester'].queryset = Semester.objects.filter(end_date__gte=timezone.now())
    def clean(self):
        cleaned_data = super(SubmitAvailabilityForm, self).clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        # it seems like we're always getting back a 
        # datetime.time object when the form gets processed
        if start_time and end_time:
            start = start_time.hour
            end = end_time.hour
            diff = end - start
            if  diff <= 0:
                msg = 'Please make sure these times are correct.'
                self.add_error('start_time', msg)
                self.add_error('end_time', msg)
            elif diff > 1:
                self._times = [time(start+i,0,0) for i in range(diff+1)]
        return cleaned_data

class AvailabilityUpdateForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ['start_time', 'end_time', 'day', 'semester']
    start_time = forms.TimeField(input_formats=ACCEPTED_FORMATS)
    end_time = forms.TimeField(input_formats=ACCEPTED_FORMATS)
    _times = list()

    def clean(self):
        cleaned_data = super(AvailabilityUpdateForm, self).clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time:
            start = start_time.hour
            end = end_time.hour
            diff = end - start
            if  diff <= 0:
                msg = 'Please make sure these times are correct.'
                self.add_error('start_time', msg)
                self.add_error('end_time', msg)
            elif diff > 1:
                msg = 'Please adjust to only be in 1 hour increments'
                self.add_error('start_time', msg)
                self.add_error('end_time' , msg)
        return cleaned_data
