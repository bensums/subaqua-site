from django.shortcuts import render, render_to_response
from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect
from events.models import Event
from events.forms import EventForm
from django.contrib.auth.decorators import login_required

def home(request):
    latest_events = Event.objects.all().order_by('-post_date')[:5]
    if request.user.is_authenticated():
        my_events = request.user.event_set.all()
    else:
        my_events = None
    return render(request, 'events/home.html',
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

@login_required
def add(request):
    if not request.user.is_staff:
        return HttpResponseForbidden() 
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            # create and save new model
            event = form.save()
            return HttpResponseRedirect('/')
    else:
        form = EventForm()

    return render(request, 'events/add.html',
                             {
                                'form': form,
                             })

