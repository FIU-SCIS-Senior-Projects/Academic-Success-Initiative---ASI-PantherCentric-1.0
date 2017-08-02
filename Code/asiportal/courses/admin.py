from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from .models import Course

class CourseAdmin(admin.ModelAdmin):
    list_display = ['name',]
    list_filter = ['team', 'name']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'team_leader':
            kwargs["queryset"] = User.objects.filter(groups__name='Team Leader')
        return super(CourseAdmin, self).formfield_for_foreignkey(db_field,request,**kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'team':
            kwargs["queryset"] = User.objects.filter(groups__name='Ambassador')
        return super(CourseAdmin, self).formfield_for_manytomany(db_field,request,**kwargs)

admin.site.register(Course, CourseAdmin)
