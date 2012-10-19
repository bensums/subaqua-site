from django.conf.urls import patterns, include, url

from django.views.generic.simple import redirect_to, direct_to_template
from django.contrib.staticfiles.storage import staticfiles_storage

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^ueasa-events/', include('ueasa-events.foo.urls')),
    url(r'^favicon.ico$', redirect_to,
        {'url': staticfiles_storage.url('favicon.ico')}),
    url(r'^$', 'events.views.home'),
    url(r'^login-error/$', direct_to_template, { 'template': 'login-error.html'
                                                }),
    url(r'^canvas/$', 'fbapp.views.canvas'),
    url(r'^events/', include('events.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('social_auth.urls')),
)
