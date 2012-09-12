from django.shortcuts import render_to_response
from events.models import Event

def home(request):
    latest_events = Event.objects.all().order_by('-post_date')[:5]
    #my_events = Events.
    return render_to_response('events/home.html',
            {'latest_events': latest_events}
    )


