from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseForbidden, \
                        HttpResponseRedirect, HttpResponseServerError
from django.core.validators import validate_slug
from django.forms import ValidationError
from events.models import Event, RSVP
from events.forms import EventForm, RSVPForm
from events.util import send_mail
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from datetime import datetime


def home(request):
    future_events = Event.objects.filter(
        start_time__gte=datetime.now()
    ).order_by('category', 'start_time')

    return render(request, 'events/home.html',
            {
                'future_events': future_events
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

    try:
        rsvp = RSVP.objects.get(event=e, user=request.user)
    except RSVP.DoesNotExist:
        rsvp = None

    if rsvp:
        # User is already registered for this event.
        return render(request, 'events/register.html', {
            'already_registered': True,
            'event': e
        })

    if request.method == 'POST':
        form = RSVPForm(request.POST)
        if form.is_valid():
            # Prepare a model instance from the form but do not save to db.
            rsvp = form.save(commit=False)
            rsvp.event = e
            rsvp.user = request.user
            rsvp.status = RSVP.REGISTERED
            # now save.
            rsvp.save()

            comment = form.cleaned_data['comment'].strip()
            if comment:
                send_mail(
                    subject='Message from %s about %s' %
                        (request.user.get_full_name(), e.name),
                    message="\r\n".join([
                        'Event: %s on %s,' % (e.name, e.start_time),
                        '',
                        'Message: %s' % comment,
                    ]),
                    reply_to=request.user.email
                )

            
            return HttpResponseRedirect(reverse('events.views.detail',
                                                args=(slug,)))
            
    else:
        form = RSVPForm()

    return render(request, 'events/register.html', {
        'form': form,
        'event': e
    })

#    RSVP.objects.get_or_create(event=e, user=request.user)
#    return HttpResponseRedirect(reverse('events.views.detail', args=(slug,)))

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

@login_required
def slug_available(request):
    if request.method == 'GET':
        if request.GET.has_key('slug'):
            slug = request.GET['slug']

            try:
                validate_slug(slug)
            except ValidationError:
                return HttpResponseServerError()

            try:
                e = Event.objects.get(slug=slug)
            except Event.DoesNotExist:
                e = None
            if e:
                # event with that slug already exists
                return HttpResponseServerError()
            return HttpResponse()
    return HttpResponseServerError("Invalid request")

