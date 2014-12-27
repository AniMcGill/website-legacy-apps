from django.db import models
from forums.models import Thread
# Create your models here.

class EventType(models.Model):
    name = models.CharField(max_length=30, unique=True)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ['name']

class Location(models.Model):
    name = models.CharField(max_length=64, unique=True)
    addr_one = models.CharField(max_length=32)
    addr_two = models.CharField(max_length=32, blank=True)
    postcode = models.CharField(max_length=6)
    city = models.CharField(max_length=32, default="Montreal")
    def ordered(self):
        addr = self.name+"<br>"+self.addr_one
        if (self.addr_two):
            addr = addr + "<br>" + self.addr_two
        addr = addr + "<br>" + self.postcode + "<br>" + self.city
        return addr
    def __unicode__(self):
        return self.name

class Event(models.Model):
    at = models.DateTimeField()
    till = models.DateTimeField()
    location = models.ForeignKey(Location)
    created = models.DateTimeField(auto_now_add = True)
    event_type = models.ForeignKey(EventType)
    name = models.CharField(max_length = 255)
    thread = models.ForeignKey(Thread)
    active = models.BooleanField(default = True)
    def __unicode__(self):
        return self.event_type.name +": "+ self.name
    @models.permalink
    def get_absolute_url(self):
        return ('event_view',(),{'ev_id': self.pk})
    def get_description(self):
        return self.thread.get_first().text_shown
    class Meta:
        ordering = ['at','name']
        get_latest_by = 'created'
