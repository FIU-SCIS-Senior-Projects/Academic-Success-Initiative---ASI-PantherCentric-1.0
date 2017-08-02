from django.contrib import admin
from .models import Videos, AltUser

# Register your models here.
class VideoAdmin(admin.ModelAdmin):
    list_display = ["title", "url_code"]
class AltUserAdmin(admin.ModelAdmin):
    list_display = ["username", "pantherID", "code_name"]

admin.site.register(Videos, VideoAdmin)
admin.site.register(AltUser, AltUserAdmin)
