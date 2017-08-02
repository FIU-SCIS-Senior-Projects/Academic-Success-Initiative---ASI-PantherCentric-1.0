import uuid
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class AccountActivationToken(models.Model):
    user = models.OneToOneField(User,
            related_name='activation_token')
    used = models.BooleanField(default=False)
    token = models.UUIDField(default=uuid.uuid4)

    def get_absolute_url(self):
        return reverse('activate_account', args=[str(self.token)])
