from django.db import models
from django.utils.crypto import get_random_string
from courses.models import Course


class PollTime(models.Model):

    DAYS = (
            (1,'Monday'),
            (2,'Tuesday'),
            (3,'Wednesday'),
            (4,'Thursday'),
            (5,'Friday'),
    )

    course = models.ForeignKey(Course,
                        related_name="course", default=1)
    time_start = models.TimeField()
    time_end = models.TimeField()
    day = models.IntegerField(choices=DAYS, default=1)
