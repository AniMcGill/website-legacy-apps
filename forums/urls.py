from django.conf.urls import patterns, include, url

urlpatterns = patterns('forums.views',
    url(r'^$', 'index', name='home'),
    url(r'^board/(?P<board>\d+)/$', 'show_board', name="board_view"),
    url(r'^board/(?P<board>\d+)/post/$', 'post_thread', name="new_thread"),
    url(r'^board/(?P<board>\d+)/(?P<page>\d+)/$', 'show_board', name="board-page_view"),
    url(r'^thread/(?P<thread>\d+)/$', 'show_thread', name="thread_view"),
    url(r'^thread/(?P<thread>\d+)/(?P<page>\d+)/$', 'show_thread', name="thread-page_view"),
    url(r'^post/(?P<post>\d+)/edit/$', 'edit_post', name="edit_post"),
    url(r'^post/(?P<post>\d+)/$', 'single_post', name="view_post"),
)
