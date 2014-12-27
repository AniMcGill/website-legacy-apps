from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^profile/$', 'MAC_profile.views.view_profile', name="self_user_view"),
    url(r'^profile/(?P<user>\d+)/$', 'MAC_profile.views.view_profile', name="user_view"),
    url(r'^login/$','django.contrib.auth.views.login',{'template_name': 'accounts/login.html'},name="login"),
    url(r'^logout/$','MAC_profile.views.logoutview',name="logout"),
    url(r'^register/$','MAC_profile.views.registration',name="register"),
    url(r'^newpass/$','MAC_profile.views.new_pass',name="new_pass"),
)
