from events.views import home
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.conf import settings
from social_auth.views import complete as social_complete
from social_auth.backends.facebook import FacebookBackend
from django.http import HttpResponseRedirect
from django.contrib.auth import BACKEND_SESSION_KEY
from social_auth.backends.exceptions import AuthException

@csrf_exempt
def canvas(request):
    # When a Facebook user first authorises our app, Facebook redirects to
    # a url with ?code=... The presence of this parameter seems to break
    # auth_complete in the facebook backend (called by social_complete). 
    # So we remove it.
    if 'code' in request.GET:
        request.GET = request.GET.copy()
        del request.GET['code']

    # Try to log in using values POSTed by Facebook.
    try:
        social_complete(request, FacebookBackend.name)
    except AuthException:
        pass

    # Check if logged in.
    if is_complete_authentication(request):
        return HttpResponseRedirect('/')

    print request.session.get(BACKEND_SESSION_KEY)

    # finally if not logged in
    auth_url = 'https://www.facebook.com/dialog/oauth?client_id={app_id}' \
    '&redirect_uri={canvas_url}&scope={scope}'.format(
        app_id=settings.FACEBOOK_APP_ID,
        canvas_url=settings.FACEBOOK_CANVAS_URL,
        scope=','.join(settings.FACEBOOK_EXTENDED_PERMISSIONS)
    )
    return render_to_response('fbapp/oauth.html', {'auth_url': auth_url})

# Checks the completeness of current user authentication; complete = logged via
# Facebook backend
def is_complete_authentication(request):
    return request.user.is_authenticated() and FacebookBackend.__name__ in \
        request.session.get(BACKEND_SESSION_KEY, '')
