from django.contrib import admin
from .models import Semester

class SemesterModelAdmin(admin.ModelAdmin):
    pass

admin.site.register(Semester, SemesterModelAdmin)
