from django.conf.urls import patterns, url

urlpatterns = patterns('events.views',
    url(r'^$', 'home'),
    url(r'^(?P<slug>[-\w]+)/$', 'detail'), 
)
