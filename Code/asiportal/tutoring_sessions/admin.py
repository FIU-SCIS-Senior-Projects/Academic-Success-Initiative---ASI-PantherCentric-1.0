from django.contrib import admin
from . import models

class SessionAdmin(admin.ModelAdmin):
    list_display = ['availability', 'tutee', 'course']
    list_filter = ['availability__semester', 'availability__ambassador', 'availability__start_time', 'availability__end_time', 'availability__day', 'tutee', 'course']

class IndividualSessionAdmin(admin.ModelAdmin):
    list_display = ['session']
    list_filter = ['session']

admin.site.register(models.Session, SessionAdmin)
admin.site.register(models.IndividualSession, IndividualSessionAdmin)
