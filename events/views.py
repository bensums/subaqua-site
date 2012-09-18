from django.shortcuts import render_to_response
from django.http import Http404
from events.models import Event

def home(request):
    latest_events = Event.objects.all().order_by('-post_date')[:5]
    if request.user.is_authenticated():
        my_events = request.user.event_set.all()
    else:
        my_events = None
    return render_to_response('events/home.html',
            {
                'latest_events': latest_events,
                'my_events': my_events
            }
        )


def detail(request, slug):
    try:
        e = Event.objects.get(slug=slug)
    except Event.DoesNotExist:
        raise Http404
    return render_to_response('events/detail.html', {'event': e})





