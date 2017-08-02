from django.db import models
from django.contrib.auth.models import User

class Videos(models.Model):

    def __str__(self):
        return self.title

    url_code = models.CharField(max_length=20)
    title = models.CharField(max_length=225)

class AltUser(models.Model):

    def __str__(self):
        return self.code_name

    username = models.ForeignKey(
            User,
            related_name = 'actual_user'
            )
    pantherID = models.IntegerField()
    code_name = models.CharField(max_length=20)
