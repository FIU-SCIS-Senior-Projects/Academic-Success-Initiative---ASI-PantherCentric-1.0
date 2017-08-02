from django.contrib import admin
from .models import TutoringRequest

class TutoringRequestAdmin(admin.ModelAdmin):
    list_display = ['availability', 'submitted_by', 'course', 'status']
    list_filter = ['status' ,'course', 'submitted_by']

admin.site.register(TutoringRequest, TutoringRequestAdmin)
