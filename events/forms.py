from django.forms import ModelForm  
from django import forms
from events.models import Event, RSVP

class EventForm(ModelForm):
    class Meta:
        model = Event 


class RSVPForm(ModelForm):
    qualified = forms.BooleanField(
        required=True,
        label="Please tick this box to confirm you are a qualified diver."
    )

    class Meta:
        model = RSVP
        exclude = ('event', 'user', 'status')


