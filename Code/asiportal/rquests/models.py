from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from availabilities.models import Availability
from courses.models import Course
from tutoring_sessions.models import Session

class TutoringRequest(models.Model):
    STATUS_CODES = (
                    ('A', 'Open'),
                    ('B', 'Scheduled'),
                    ('C', 'Canceled'),
                    ('D', 'No Room Available'),
                    )
    submitted_by = models.ForeignKey(User,
                    related_name='tutoring_requests')
    availability = models.ForeignKey(Availability,
                    related_name='requests')
    course = models.ForeignKey(Course,
            related_name='course_requests')
    status = models.CharField(choices=STATUS_CODES, default='A',
                              max_length=1)
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        if self.status != 'A':
            self.updated_at = timezone.now()
        super(TutoringRequest, self).save(*args, **kwargs)

    def __str__(self):
        return '%s with %s from %s' % (self.course,
                                       self.availability,
                                       self.submitted_by.get_full_name())

class SessionCancelationRequest(models.Model):
    STATUS_CODES = (
            ('A', 'Unresolved'),
            ('B', 'Completed'),
            ('C', 'Canceled'),
            )

    session = models.ForeignKey(Session,
            related_name='cancelation_requests'
            )
    reason = models.CharField(max_length=255)
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    status = models.CharField(choices=STATUS_CODES, default='A',
                              max_length=1)
