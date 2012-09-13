import json
import base64
import hmac
import hashlib

from django.conf import settings

class IgnoreFbCsrfMiddleware(object):
    """From http://djangosnippets.org/snippets/2272/
       See https://developers.facebook.com/docs/canvas/post/
       """

    def process_request(self, request):
        signed_request = request.REQUEST.get('signed_request', None)
        # If no signed_request then do nothing.
        if signed_request == None:
            return
        signed_request = fb_decode_signed_request(signed_request, settings.FACEBOOK_API_SECRET)
        request.csrf_processing_done = signed_request != None


def b64url_decode(encoded):
    """Decode a string encoded in URL-safe base64 without padding."""
    # The padding should round the length of the string up to a multiple of 4.
    padding_fixed = encoded + (-len(encoded) % 4) * '='
    return base64.urlsafe_b64decode(padding_fixed)

def fb_decode_signed_request(signed_request, app_secret):
    """Decode Facebook's signed_request. Fail if signature cannot be verified since this indicates the request likely does not originate from Facebook."""
    sig, payload = str(signed_request).split('.', 1)

    data = json.loads(b64url_decode(payload))
    
    if not data['algorithm'].upper() == 'HMAC-SHA256':
        raise ValueError('unknown algorithm {0}'.format(data['algorithm']))

    h = hmac.new(app_secret, digestmod=hashlib.sha256)
    h.update(payload)
    expected_sig = base64.urlsafe_b64encode(h.digest()).replace('=', '')

    if sig != expected_sig:
        print 'sig: ' + sig
        print 'expected_sig: ' + expected_sig
        raise ValueError('bad signature')

    return data

