from django import forms
from .models import UserProfile

class UserProfileCreateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('sex', 'major', 'phone_number')
