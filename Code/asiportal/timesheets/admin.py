from django.contrib import admin
from django.contrib.auth.models import User
from .models import TimeSheet, TutoringTimeSheetEntry

class TimeSheetAdmin(admin.ModelAdmin):
    list_display = ['ambassador', 'pay_period_begin', 'pay_period_end']
    list_filter = ['ambassador', 'pay_period_begin', 'pay_period_end']

class TutoringTimeSheetEntryAdmin(admin.ModelAdmin):
    list_display = ['session', 'timesheet', 'tl_verified', ]
    list_filter = ['tl_verified', 'session__session__ambassador', 'timesheet', 'session__session_date', 'timesheet']

admin.site.register(TimeSheet, TimeSheetAdmin)
admin.site.register(TutoringTimeSheetEntry, TutoringTimeSheetEntryAdmin)
