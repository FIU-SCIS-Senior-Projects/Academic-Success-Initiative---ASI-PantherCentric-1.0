from django.core.validators import RegexValidator
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


'''
As wanted by the product owner, the user profile should contain:
    Sex
    Major
    Phone #
Should be a 1 to 1 relation.
'''
SEXS = (
        ('F', 'Female'),
        ('M', 'Male'),
        )

MAJORS = (
        ('CS', 'Computer Science'),
        ('IT', 'Information Technology'),
        )

class UserProfile(models.Model):
    user = models.OneToOneField(
            settings.AUTH_USER_MODEL,
            related_name='profile')
    sex = models.CharField(choices=SEXS, default='M', max_length=2)
    major = models.CharField(choices=MAJORS, default='CS', max_length=2)
    phone_number_regex = RegexValidator(regex=r'^\d{10}$', message="Phone Numbers must be entered in the format : 3053482000")
    phone_number = models.CharField(validators=[phone_number_regex], max_length=10)
