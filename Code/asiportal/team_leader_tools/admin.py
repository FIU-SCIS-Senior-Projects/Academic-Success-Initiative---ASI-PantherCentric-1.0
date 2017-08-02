from django.contrib import admin
from .models import PollTime

# Register your models here.

class PollTimeAdmin(admin.ModelAdmin):
    list_display = ['course', 'time_start', 'time_end', 'day']

admin.site.register(PollTime, PollTimeAdmin )
