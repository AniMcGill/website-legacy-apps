from events.models import Event
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.core.exceptions import PermissionDenied
from datetime import datetime, date
import calendar
import pytz
# Create your views here.

def index(request):
    events = Event.objects.filter(active=True, at__gte=datetime.now(pytz.timezone('US/Eastern')))
    return render_to_response('events/index.html', {'events': events}, context_instance=RequestContext(request))

def event_list(request):
    now=datetime.now(pytz.timezone('US/Eastern'))
    upcoming = Event.objects.filter(active=True, at__gte=now)
    past = Event.objects.filter(active=True, at__lt=now)
    today = Event.objects.filter(active=True, at__year=now.year, at__month=now.month, at__day=now.day)
    return render_to_response('events/list.html', {'upcoming': upcoming, 'past': past, 'today':today}, context_instance=RequestContext(request))

def event(request,ev_id):
    event = get_object_or_404(Event, pk=ev_id)
    return render_to_response('events/event.html', {'event': event}, context_instance=RequestContext(request))

def cal(request, year=None, month=None):
    if not (year or month):
        date = date.today()
    else: 
        try: 
            date = date(year,month)
        except:
            return render_to_response('events/bad_date.html', context_instance=RequestContext(request))
    events = Event.objects.filter(at__year=date.year, at__month=date.month)
    cal = calendar.Calendar().monthdatescalendar(date.year,date.month)
    return render_to_response('events/cal.html', {'events': events, 'cal': cal, 'month': calendar.month_name[date.month]}, context_instance=RequestContext(request))
