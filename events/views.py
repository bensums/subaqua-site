from django.shortcuts import render, render_to_response
from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect
from events.models import Event, RSVP
from events.forms import EventForm
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

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
    # is user signed up?
    user_status = None
    if request.user.is_authenticated():
        if request.user in e.people.all():
            user_status = 'REGISTERED'
        else:
            user_status = 'NOT_REGISTERED'

    return render(request, 'events/detail.html', {
        'event': e,
        'user_status': user_status
                                                    })

@login_required
def register(request, slug):
    try:
        e = Event.objects.get(slug=slug)
    except Event.DoesNotExist:
        raise Http404
    RSVP.objects.get_or_create(event=e, user=request.user)
    return HttpResponseRedirect(reverse('events.views.detail', args=(slug,)))

@login_required
def unregister(request, slug):
    try:
        e = Event.objects.get(slug=slug)
    except Event.DoesNotExist:
        raise Http404
    # It doesn't matter if not registered, this next line is idempotent
    # and cheaper not to check if registered.
    request.user.rsvp_set.filter(event=e).delete()
    return HttpResponseRedirect(reverse('events.views.detail', args=(slug,)))

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

