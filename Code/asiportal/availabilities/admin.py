from django.contrib import admin
from availabilities.models import Availability

class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ['ambassador', 'day', 'start_time', 'end_time', 'is_scheduled', 'semester']
    list_filter = ['ambassador', 'day', 'start_time', 'end_time', 'semester', 'is_scheduled']
admin.site.register(Availability, AvailabilityAdmin)
