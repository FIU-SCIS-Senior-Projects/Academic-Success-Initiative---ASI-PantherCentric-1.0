from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'major', 'sex', 'phone_number']
    list_filter = ['major', 'sex']

admin.site.register(UserProfile, UserProfileAdmin)
