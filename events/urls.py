from django.conf.urls import patterns, url

urlpatterns = patterns('events.views',
    url(r'^$', 'home'),
    url(r'^add/$', 'add'),
    url(r'^slug_available/$', 'slug_available'),
    url(r'^(?P<slug>[-\w]+)/$', 'detail'), 
    url(r'^(?P<slug>[-\w]+)/register/$', 'register'), 
    url(r'^(?P<slug>[-\w]+)/unregister/$', 'unregister'), 
)
