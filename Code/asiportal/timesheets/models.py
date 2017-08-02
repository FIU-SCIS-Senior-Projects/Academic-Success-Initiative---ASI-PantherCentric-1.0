import json
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import models
from tutoring_sessions.models import IndividualSession
from channels import Group
'''
A time sheet should be defined as 
a collection of entries
so conceptually a timesheet ( in the singular ) does not exist
and shouldn't exist as it would just be a grouping of individual entries
'''
class TimeSheet(models.Model):
    class Meta:
        permissions = (
                ("approve_timesheet", "Can approve timesheet"),
                )

    pay_period_begin = models.DateField()
    pay_period_end = models.DateField()
    ambassador = models.ForeignKey(
            User, related_name='timesheets',
            limit_choices_to={'is_staff' : True})
    final_approval = models.BooleanField(default=False)
    date_submitted = models.DateTimeField(auto_now_add=True)
    date_approved = models.DateTimeField(auto_now_add=True)

    @property
    def group_name(self):
        return 'timesheet-{}'.format(self.pk)

    def __str__(self):
        return '{} timesheet for {} to {}'.format(
                self.ambassador.get_full_name(),
                self.pay_period_begin,
                self.pay_period_end,
                )

class ProjectTimeSheetEntry(models.Model):
    class Meta:
        permissions = (
                ("approve_entry", "Can Approve Entries"),
                )

    description = models.CharField(max_length=150, default="")
    project_time_sheet = models.ForeignKey(TimeSheet,
            related_name='project_entries')
    project_leader = models.ForeignKey(User, related_name="projects_to_approve")
    title = models.CharField(max_length=16, default="")
    project_lead_verified = models.BooleanField(default=False)
    title = models.CharField(max_length=16, default="")
    total_time = models.IntegerField(default=0)
    start_time = models.TimeField(default=timezone.now)
    end_time = models.TimeField(default=timezone.now)
    day = models.DateField(default=timezone.now)

class TutoringTimeSheetEntry(models.Model):
    class Meta:
        permissions = (
                ("approve_entry", "Can Approve Entries"),
                )
        unique_together = ('session', 'timesheet')

    timesheet = models.ForeignKey(TimeSheet, related_name='entries')
    session = models.ForeignKey(IndividualSession,
            related_name='accounted_hours') 
    total_time = models.IntegerField(default=0) # for a session should always be 1 or 0 ( at least right now )
    tl_verified = models.BooleanField(default=False)

    # def clean(self):
    #     if self.total_time < 0 or self.total_time > 1:
    #         raise ValidationError(_('Tutoring sessions are only an hour long! Please contact your team leader if you wish to have a manual override'))
    #     if self.date < self.timesheet.pay_period_begin or self.date > self.timesheet.pay_period_end:
    #         raise ValidationError(_('This session did not take place during the designated pay period.'))

    def send_notification(self, created=False, deleted=False):
        notification = {
                "created" : created,
                "deleted" : deleted,
                "id" : self.id,
                "sess_id" : self.session.id,
                "start_time" : self.session.session.start_time.strftime('%I:%M %p'),
                "end_time" : self.session.session.end_time.strftime('%I:%M %p'),
                "sdate" : self.session.session_date.strftime('%b, %e %Y'),
                "session": self.session.__str__(),
                "total_time" : self.total_time,
                "tl_verified" : self.tl_verified,
                }
        Group(self.timesheet.group_name).send({
                    "text" : json.dumps(notification),
            })

    def save(self, *args, **kwargs):
        result = super(TutoringTimeSheetEntry, self).save(*args, **kwargs)
        self.send_notification(created=True)
        return result

    def delete(self, *args, **kwargs):
        self.send_notification(deleted=True)
        super(TutoringTimeSheetEntry, self).delete(*args, **kwargs)
