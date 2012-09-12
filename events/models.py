from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    name = models.CharField(max_length=200)
    post_date = models.DateTimeField('Post time', auto_now_add=True)
    date = models.DateTimeField('Event time')
    people = models.ManyToManyField(User)

    def __unicode__(self):
        return self.name


