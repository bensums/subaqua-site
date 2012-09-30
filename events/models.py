from django.db import models
from django.contrib.auth.models import User

class EventCategory(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True, unique=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        verbose_name_plural = "event categories"

    def __unicode__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=210, unique=True)
    description = models.TextField(default='', blank=True)
    category = models.ForeignKey('EventCategory', null=True, blank=True)
    post_date = models.DateTimeField('Post time', auto_now_add=True,
                                     null=True, blank=True,
                                     help_text='YYYY-MM-DD hh:mm:ss')
    start_time = models.DateTimeField('Start time',
                                      help_text='YYYY-MM-DD hh:mm:ss')
    end_time = models.DateTimeField('End time', default=None, null=True,
                                    blank=True,
                                    help_text='YYYY-MM-DD hh:mm:ss',
                                    )
    people = models.ManyToManyField(User, null=True, blank=True, through='RSVP')
    max_people = models.PositiveIntegerField(null=True, blank=True,
                                             default=None)
    cost = models.PositiveIntegerField(default=0)
    location = models.CharField(max_length=250, null=True, blank=True,
                                default=None)

    def __unicode__(self):
        return self.name

    def attendees(self):
        """
        Return list of users registered for event who were early enough to get
        a place in the first-come-first-served list.
        """
        if not self.max_people:
            return self.people.all()
        return self.people.order_by('rsvp__registration_time')[:self.max_people]

    def wannabes(self):
        """
        Return list of users registered for the event but too late to get in
        due to first-come-first-served nature of events.
        """
        if not self.max_people:
            return []
        return self.people.order_by('rsvp__registration_time')[self.max_people:]


class RSVP(models.Model):
    REGISTERED = 'R'
    UNREGISTERED = 'U'

    event = models.ForeignKey(Event)
    user = models.ForeignKey(User)
    registration_time = models.DateTimeField(
        help_text='YYYY-MM-DD hh:mm:ss',
        auto_now_add=True,
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=2,
        choices=((REGISTERED, 'Registered'),
                 (UNREGISTERED, 'Not registered')),
        null=True,
        blank=True,
        default=REGISTERED
    )
    comment = models.TextField(
        blank=True,
        default="",
        help_text="If you have a message for the organisers, enter it here \
        and they will get back to you."
    )


from django.conf import settings

from djangogcal.adapter import CalendarAdapter, CalendarEventData
from djangogcal.observer import CalendarObserver

class EventCalendarAdapter(CalendarAdapter):
    def get_event_data(self, instance):
        return CalendarEventData(
            start=instance.start_time,
            end=instance.end_time,
            title=instance.name,
            content=instance.description
        )

observer = CalendarObserver(email=settings.CALENDAR_EMAIL,
                            password=settings.CALENDAR_PASSWORD)
observer.observe(Event, EventCalendarAdapter())


