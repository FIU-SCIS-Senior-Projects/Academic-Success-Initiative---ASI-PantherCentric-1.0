from django.contrib import admin
from .models import AmbassadorSurvey, TuteeSurvey

myModels = [AmbassadorSurvey, TuteeSurvey]

class SurveyAdmin(admin.ModelAdmin):
    list_display = ['individual_session', 'submitted_at' ]
    list_filter = ['individual_session__session', 'submitted_at', 'submitted', 'individual_session__session_date']

admin.site.register(myModels, SurveyAdmin)
