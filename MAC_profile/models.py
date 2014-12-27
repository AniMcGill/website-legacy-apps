from django.db import models
from django.contrib.auth.models import User, Group
from forums.models import Category
from django.db.models.signals import post_save
from postmarkup import render_bbcode
import markdown

# Create your models here.
# Choices
GENDERS = (
    (0, 'Not Stated'),
    (1, 'Male'),
    (2, 'Female'),
)

class Profile(models.Model):
    # User Account for Profile
    user = models.OneToOneField(User)
    
    # Actual Profile
    display_name = models.CharField(max_length=50)
    tpp = models.PositiveSmallIntegerField(default=25)
    ppp = models.PositiveSmallIntegerField(default=10)
    avatar_local = models.ImageField(upload_to="avatars/",blank=True, null=True)
    blurb = models.CharField(max_length=255, blank=True)
    sig = models.TextField(max_length=300,blank=True)
    sig_shown = models.TextField(blank=True)
    website_url = models.URLField(blank=True)
    website_text = models.CharField(max_length = 255, blank=True)
    steam_account = models.CharField(max_length = 30, blank = True)
    psn_account = models.CharField(max_length = 16, blank = True)
    xbox_account = models.CharField(max_length = 20, blank = True)
    msn_account = models.CharField(max_length = 255, blank = True)
    yim_account = models.CharField(max_length = 32, blank = True)
    aim_account = models.CharField(max_length = 255, blank = True)
    icq_account = models.CharField(max_length = 255, blank = True)
    location = models.CharField(max_length = 255, blank = True)
    gender = models.PositiveSmallIntegerField(choices=GENDERS, default=0)
    timezone = models.CharField(max_length = 255, blank = True)
    group = models.ForeignKey( 'GroupProfile' )
    pass_reset_code = models.CharField(max_length = 200, blank=True)
    def __unicode__(self):
        return self.user.username
    @models.permalink
    def get_absolute_url(self):
        return ('user_view',(),{'user': self.user.pk})
    def save(self, **kwargs):
        self.sig_shown = render_bbcode(self.sig)
        super(Profile, self).save(**kwargs)
    def avatar(self):
        if self.avatar_local:
            url = self.avatar_local.url
        else:
            url = "/static/profile/no_avatar.png"
        return url

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, group_id=1, display_name=instance.username)

post_save.connect(create_user_profile, sender=User)

class GroupProfile(models.Model):
    allowed_read = models.ManyToManyField(Category, related_name = "can_view", blank = True)
    allowed_post = models.ManyToManyField(Category, related_name = "can_post", blank = True)
    allowed_reply= models.ManyToManyField(Category, related_name = "can_reply", blank = True)
    leader = models.ForeignKey( User , blank = True, null = True)
    description = models.CharField(max_length = 300, blank = True)
    group = models.ForeignKey( Group )
    def __unicode__(self):
        return self.group.name

def create_group_profile(sender, instance, created, **kwargs):
    if created:
        GroupProfile.objects.create(group=instance)

post_save.connect(create_group_profile, sender=Group)

class MAC_extra_user(models.Model):
    user = models.OneToOneField(User)
    joomla_id = models.PositiveIntegerField(default=0)
    phpbb_id = models.PositiveIntegerField(default=0)

class Exec(models.Model):
    user = models.ForeignKey(User)
    position = models.CharField(max_length = 30)
    fav = models.CharField(max_length = 64)
    about = models.TextField()
    about_saved = models.TextField(null=True)
    active = models.BooleanField(default=True)

    def name(self):
        return self.user.get_full_name()

    def __unicode__(self):
        return self.position +": " + self.user.first_name

    def save(self, **kwargs):
        self.about_saved = markdown.markdown(self.about)
        super(Exec, self).save(**kwargs)

    def get_absolute_url(self):
        return self.user.profile.get_absolute_url()

    class Meta:
        ordering = ['position'] # sort by posistion name, This means President comes 1st, as P < V
