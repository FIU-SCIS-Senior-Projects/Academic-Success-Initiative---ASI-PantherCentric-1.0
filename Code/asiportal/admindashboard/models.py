# Django
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Note(models.Model):
    note = models.CharField(max_length=140)
    created = models.DateTimeField(auto_now=True)
    tutee = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notes')

class Review(models.Model):
	tutee = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='review')
	reviewed = models.BooleanField(default=False)
