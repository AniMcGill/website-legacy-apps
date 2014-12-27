from django.conf.urls import patterns, include, url

urlpatterns = patterns('events.views',
    #url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', 'show_date', name="month_view"),
    #url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', 'show_date', name="day_view"),
    url(r'^calendar/$', 'cal', name="calendar_now"),
    url(r'^list/$', 'event_list', name="event_list"),
    url(r'^calendar/(?P<year>\d{4})/(?P<month>\d{2})/$', 'cal', name="calendar"),
    url(r'^event/(?P<ev_id>\d+)/$', 'event', name="event_view"),
)
# Flat pages go here...
urlpatterns += patterns('django.contrib.flatpages.views',
    url(r'^$', 'flatpage', {'url': '/about/events/'}, name='about_events'),
)