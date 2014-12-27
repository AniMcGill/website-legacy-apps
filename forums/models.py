from django.db import models
from django.contrib.auth.models import User
import attachments.models
from postmarkup import render_bbcode
from datetime import datetime
import pytz

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length = 150)
    description = models.CharField(max_length = 300)
    parent = models.ForeignKey('self', null=True, blank=True)
    last = models.DateTimeField(auto_now = True)
    anon_viewable = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=0)
    def post_count(self):
        posts = 0
        for sub in self.category_set.all():
            posts += sub.post_count()
        for thread in self.thread_set.all():
            posts += thread.post_count()
        return posts
    def __unicode__(self):
        return self.name
    def last_thread(self):
        return self.thread_set.order_by('-created')[0]
    def last_post(self):
        return self.thread_set.order_by('-last')[0].get_last()
    @models.permalink
    def get_absolute_url(self):
        return ('board_view',(),{'board': self.pk})
    def menu_id(self):
        return "menu_forum_"+str(self.id)
    def getReadTracker(self, user):
        tracker = self.userboardread_set.filter(user=user)
        if tracker:
            return tracker[0]
        else:
            tracker = UserBoardRead(board=self, user = user)
            tracker.last_read=tracker.last_read.replace(tzinfo=pytz.utc)
            tracker.save()
            return tracker
    def save(self, **kwargs): #tell the parent, if it exists that it has been updated
        if self.parent:
            self.parent.save()
        super(Category, self).save(**kwargs)
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['order', 'name']

class Thread(models.Model):
    subject = models.CharField(max_length = 255)
    creator = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add= True)
    last = models.DateTimeField(auto_now = True)
    locked = models.BooleanField(default = False)
    sticky = models.BooleanField(default = False)
    category = models.ForeignKey(Category)
    old_id = models.IntegerField(null=True)
    hidden = models.BooleanField(default = False)
    def __unicode__(self):
        return self.subject
    def has_poll(self):
        return self.poll_set.count() > 0
    has_poll.boolean = True
    def post_count(self):
        return self.post_set.count()
    def reply_count(self):
        return self.post_set.count() - 1
    def get_first(self):
        return self.post_set.order_by('pk')[0]
    def get_last(self):
        return self.post_set.order_by('-pk')[0]
    def save(self, **kwargs): #tell the board that it has been updated
        self.category.save()
        super(Thread, self).save(**kwargs)
    @models.permalink
    def get_absolute_url(self):
        return ('thread_view',(), {'thread': self.pk})
    class Meta:
        get_latest_by = "created"
        ordering = ['-last']
    def getReadTracker(self, user):
        tracker = self.userthreadread_set.filter(user=user)
        if tracker:
            return tracker[0]
        else:
            tracker = UserThreadRead(thread=self, user = user)
            tracker.last_read=tracker.last_read.replace(tzinfo=pytz.utc)
            tracker.save()
            return tracker
    class Meta:
        order_with_respect_to = 'category'
        ordering = ['last']

class Post(models.Model):
    user = models.ForeignKey(User)
    thread = models.ForeignKey(Thread)
    created = models.DateTimeField(auto_now_add= True)
    last = models.DateTimeField(auto_now = True)
    text = models.TextField()
    text_shown = models.TextField()
    def __unicode__(self):
        return self.thread.subject +" - "+ str(self.pk)
    @models.permalink
    def get_absolute_url(self):
        return ('forums.views.single_post',(), {'post':self.pk})
    def save(self, **kwargs):
        self.text_shown = render_bbcode(self.text)
        self.thread.save()
        super(Post, self).save(**kwargs)
    class Meta:
        ordering = ['id']
        get_latest_by = "created"
        order_with_respect_to = 'thread'
        permissions = (("can_moderate", "Can Moderate the Forum"),)
        


class Attachment(attachments.models.Attachment):
    post = models.ForeignKey(Post)

class Poll(models.Model):
    question = models.CharField(max_length = 255)
    thread = models.ForeignKey(Thread)
    def get_votes(self):
        return PollVote.objects.filter(vote__poll = self)
    def __unicode__(self):
        return self.question

class PollChoice(models.Model):
    answer = models.CharField(max_length = 50)
    poll = models.ForeignKey(Poll)
    def __unicode__(self):
        return self.answer

class PollVote(models.Model):
    user = models.ForeignKey(User)
    vote = models.ForeignKey(PollChoice)
    def __unicode__(self):
        return self.user.username + " - " + self.vote.answer

class UserThreadRead(models.Model):
    user = models.ForeignKey(User)
    thread = models.ForeignKey(Thread)
    last_read = models.DateTimeField(default=datetime.min)
    def unread(self):
        return self.last_read < self.thread.last
    def update(self):
        self.last_read = datetime.now(pytz.utc)
        self.save()
    def __unicode__(self):
        return str(self.id)+"-"+self.user.username+"-"+self.thread.subject

class UserBoardRead(models.Model):
    user = models.ForeignKey(User)
    board = models.ForeignKey(Category)
    last_read = models.DateTimeField(default=datetime.min)
    def unread(self):
        return self.last_read < self.board.last
    def update(self):
        self.last_read = datetime.now(pytz.utc)
        self.save()
    def __unicode__(self):
        return str(self.id)+"-"+self.user.username+"-"+self.board.name
