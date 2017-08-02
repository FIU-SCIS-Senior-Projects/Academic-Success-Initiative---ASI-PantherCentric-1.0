from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from timesheets.models import TimeSheet
from channels import Group


class ProjectTS(models.Model):
    class Meta:
        permissions = (
                ("approve_project_ts", "Can approve timesheet"),
                )

    pay_period_begin = models.DateField()
    pay_period_end = models.DateField()
    ambassador = models.ForeignKey(
            User, related_name='project_ts_member',
            limit_choices_to={'is_staff' : True})
    ambassador_finalized = models.BooleanField(default=False)
    final_approval = models.BooleanField(default=False)
    date_submitted = models.DateTimeField(auto_now_add=True)
    date_approved = models.DateTimeField(auto_now_add=True)


class ProjectTSEntry(models.Model):
    description = models.CharField(max_length=150, default="")
    project_time_sheet = models.ForeignKey(ProjectTS, related_name="project_time_sheet")
    project_leader = models.ForeignKey(User, related_name="pl",
            limit_choices_to={'is_staff' : True, 'groups__name' : 'Team Leader'})
    project_leader_verification = models.BooleanField(default=False)
    title = models.CharField(max_length=16, default="")
    total_time = models.IntegerField(default=0)
    start_time = models.TimeField(default=timezone.now)
    end_time = models.TimeField(default=timezone.now)
    day = models.DateField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.total_time = self.end_time.hour - self.start_time.hour
        result = super(ProjectTSEntry, self).save(*args, **kwargs)
        return result
