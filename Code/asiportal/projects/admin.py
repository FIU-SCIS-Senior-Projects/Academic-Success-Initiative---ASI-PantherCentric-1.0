from django.contrib import admin
from django.contrib.auth.models import User
from .models import ProjectTS, ProjectTSEntry

class ProjectTSAdmin(admin.ModelAdmin):
    list_display = ['ambassador', 'pay_period_begin', 'pay_period_end']
    list_filter = ['ambassador', 'pay_period_begin', 'pay_period_end']

class ProjectTSEntryAdmin(admin.ModelAdmin):
    list_display = ['project_leader', 'start_time', 'title']
    list_filter = ['project_leader', 'start_time', 'title']

admin.site.register(ProjectTS, ProjectTSAdmin)
admin.site.register(ProjectTSEntry, ProjectTSEntryAdmin)
# Register your models here.
