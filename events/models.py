from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=210)
    post_date = models.DateTimeField('Post time', auto_now_add=True, null=True)
    start_time = models.DateTimeField('Start time')
    end_time = models.DateTimeField('End time', null=True, blank=True)
    people = models.ManyToManyField(User, null=True, blank=True)

    def __unicode__(self):
        return self.name

from django.conf import settings

from djangogcal.adapter import CalendarAdapter, CalendarEventData
from djangogcal.observer import CalendarObserver

class EventCalendarAdapter(CalendarAdapter):
    def get_event_data(self, instance):
        return CalendarEventData(
            start=instance.start_time,
            end=instance.end_time,
            title=instance.name
        )

observer = CalendarObserver(email=settings.CALENDAR_EMAIL,
                            password=settings.CALENDAR_PASSWORD)
observer.observe(Event, EventCalendarAdapter())


