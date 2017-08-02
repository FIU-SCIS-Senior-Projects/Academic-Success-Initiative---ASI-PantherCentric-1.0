from django import forms
from django.contrib import admin
from .models import TimeRestriction
from django.contrib.auth.models import User

# Register your models here.

class TimeRestrictionAdminForm(forms.ModelForm):
    class Meta:
        model = TimeRestriction
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TimeRestrictionAdminForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(groups__name='Ambassador')
        self.fields['user'].label_from_instance = lambda obj : obj.get_full_name()

class TimeRestrictionModelAdmin(admin.ModelAdmin):
    list_display  = ['full_name', 'max_time']
    form = TimeRestrictionAdminForm

    def full_name(self, obj):
        return obj.user.get_full_name()


    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == 'user':
    #         kwargs["queryset"] = User.objects.filter(groups__name='Ambassador')
    #     return super(TimeRestrictionModelAdmin, self).formfield_for_foreignkey(db_field,request,**kwargs)

admin.site.register(TimeRestriction, TimeRestrictionModelAdmin)
