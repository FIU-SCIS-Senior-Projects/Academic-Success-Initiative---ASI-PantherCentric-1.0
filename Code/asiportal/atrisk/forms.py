from .models import AltUser
from django import forms
from django.contrib.auth.models import User

class CreateAltUserForm(forms.ModelForm):
    class Meta:
        model = AltUser
        fields = ['username', 'pantherID', 'code_name']
    def __init__(self, *args, **kwargs):
        super(CreateAltUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].queryset = User.objects.filter(is_active=True).order_by('username')
