from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=10)
    team = models.ManyToManyField(User,
                                  related_name='courses',
                                  blank=True)
    professor = models.CharField(max_length=25,
            blank=True)
    team_leader = models.ForeignKey(
            User,
            related_name='teams',
            default=1,
            )
    slug = models.SlugField(max_length=45, blank=True)

    def __str__(self):
        if self.professor:
            return '{} with {}'.format(self.name, self.professor)
        else:
            return '{}'.format(self.name)

    def get_team_pks(self):
        team_pks = [member.pk for member in self.team.all()]
        return team_pks

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.__str__())
        super(Course, self).save(*args, **kwargs)
