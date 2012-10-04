from django.forms import ModelForm
from django import forms
from events.models import Event, RSVP
from events.widgets import JQuerySplitDateTime


class EventForm(ModelForm):
    start_time = forms.DateTimeField(
        widget=JQuerySplitDateTime
    )

    end_time = forms.DateTimeField(
        widget=JQuerySplitDateTime
    )

    class Meta:
        model = Event
        exclude = ('people',)


class RSVPForm(ModelForm):
    qualified = forms.BooleanField(
        required=True,
        label="Please tick this box to confirm you are a qualified diver."
    )

    class Meta:
        model = RSVP
        exclude = ('event', 'user', 'status')
