from django import forms

from . import models


class AmbassadorSurveyForm(forms.ModelForm):
    CHOICES = (
            (5,'Strongly Agree'),
            (4,'Agree'),
            (3,'Neutral'),
            (2,'Disagree'),
            (1,'Strongly Disagree'),
            )

    class Meta:
        model = models.AmbassadorSurvey
        fields = [
              'rating_1',
              'rating_2',
              'rating_3',
              'comments',
              'session_canceled',
              'tutee_absent',
              'canceled_session_reason',
        ]

    def __init__(self, *args, **kwargs):
        super(AmbassadorSurveyForm, self).__init__(*args, **kwargs)
        self.fields['rating_1'] = forms.ChoiceField(choices=self.CHOICES)
        self.fields['rating_2'] = forms.ChoiceField(choices=self.CHOICES)
        self.fields['rating_3'] = forms.ChoiceField(choices=self.CHOICES)
        self.fields['rating_1'].label = "Student Has Made Great Progress During Session"
        self.fields['tutee_absent'].label = 'Was the student absent?'
        self.fields['rating_2'].label = "Student Shows Good Study Skills"
        self.fields['rating_3'].label = "Student Came Prepared for Session"
        self.fields['session_canceled'].label = 'Was the session canceled?'
        self.fields['canceled_session_reason'].label = 'If the session was canceled why was it canceled'
        self.fields['canceled_session_reason'].help_text = 'Required when the session was canceled'


    def clean(self):
        cleaned_data = super().clean()
        session_canceled = cleaned_data.get('session_canceled')
        tutee_absent = cleaned_data.get('tutee_absent')
        canceled_session_reason = cleaned_data.get('canceled_session_reason')

        if session_canceled and not canceled_session_reason:
            raise forms.ValidationError(
                    "Please give a reason for session cancelation"
                    )

    def save(self, commit=True):
        survey = super(AmbassadorSurveyForm, self).save(commit=False)
        survey.submitted = True
        if commit:
            survey.save()
        return survey


class TuteeSurveyForm(forms.ModelForm):
    CHOICES = (
            (5,'Strongly Agree'),
            (4,'Agree'),
            (3,'Neutral'),
            (2,'Disagree'),
            (1,'Strongly Disagree'),
            )

    class Meta:
        model = models.TuteeSurvey
        fields = [
              'rating_1',
              'rating_2',
              'rating_3',
              'rating_4',
              'rating_5',
              'rating_6',
              'rating_7',
              'wearing_shirt',
              'comments',
        ]

    def __init__(self,*args,**kwargs):
        super(TuteeSurveyForm, self).__init__(*args,**kwargs)
        self.fields['rating_1'] = forms.ChoiceField(choices=self.CHOICES)
        self.fields['rating_2'] = forms.ChoiceField(choices=self.CHOICES)
        self.fields['rating_3'] = forms.ChoiceField(choices=self.CHOICES)
        self.fields['rating_4'] = forms.ChoiceField(choices=self.CHOICES)
        self.fields['rating_5'] = forms.ChoiceField(choices=self.CHOICES)
        self.fields['rating_6'] = forms.ChoiceField(choices=self.CHOICES)
        self.fields['rating_7'] = forms.ChoiceField(choices=self.CHOICES)
        self.fields['rating_1'].label = "It is clear the ambassador knows and understands the subject matter of this course"
        self.fields['rating_2'].label = "The ambassador explains ideas and concepts clearly."
        self.fields['rating_3'].label = "The ambassador asks me questions and has me work sample problems."
        self.fields['rating_4'].label = "The ambassador listens to me and tries to understand my problems."
        self.fields['rating_5'].label = "The ambassador is friendly and courteous with me."
        self.fields['rating_6'].label = "The ambassador is trying to accommodate my learning style."
        self.fields['rating_7'].label = "The session is helpful and improved my understanding of the subject."
        self.fields['wearing_shirt'].label = "Was your ambassador wearing an FIU/ASI related shirt?"

    def save(self, commit=True):
        survey = super(TuteeSurveyForm, self).save(commit=False)
        survey.submitted = True
        if commit:
            survey.save()
        return survey

