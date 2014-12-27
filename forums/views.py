from django.shortcuts import get_object_or_404, render_to_response
from forums.models import *
from forums.forms import PostForm, ThreadForm
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
# Create your views here.

def index(request):
    return render_to_response('forums/index.html', context_instance=RequestContext(request))

def show_board(request, board, page=1):
    board = get_object_or_404(Category, pk=board)
    sub_boards = board.category_set.all()
    if request.user.is_authenticated():
        profile = request.user.get_profile()
        threads_per_page = profile.tpp
        if board not in profile.group.allowed_read.all():
            raise PermissionDenied
        tracker = board.getReadTracker(request.user)
        tracker.update()
    else:
        profile = None
        threads_per_page = 25
        if not board.anon_viewable:
            raise PermissionDenied
    pages = Paginator(board.thread_set.all().order_by('-last'),threads_per_page)
    try:
        threads = pages.page(page)
    except PageNotAnInteger:
        threads = pages.page(1)
    except EmptyPage:
        threads = pages.page(pages.num_pages)
    return render_to_response('forums/board.html',{'board':board, 'sub_boards':sub_boards, 'threads':threads}, context_instance=RequestContext(request))

def show_thread(request, thread, page=1):
    thread = get_object_or_404(Thread, pk=thread)
    if request.method == 'GET':
        form = None
        if request.user.is_authenticated():
            posts_per_page = request.user.profile.ppp
            if thread.category in request.user.profile.group.allowed_reply.all():
                if not thread.locked:
                    form = PostForm({'thread_id':thread.id})
            if thread.category not in request.user.profile.group.allowed_read.all():
                raise PermissionDenied
            tracker = thread.getReadTracker(request.user)
            tracker.update()
        else:
            posts_per_page = 10
            if not thread.category.anon_viewable :
                raise PermissionDenied
    elif request.method == 'POST':
        if not request.user.is_authenticated() or thread.locked :
            return HttpResponseRedirect(reverse('thread-page_view', args=(thread.id,page)))
        form = PostForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['thread_id'] != thread.id:
                raise PermissionDenied
            post = Post(user = request.user, thread = thread, text = form.cleaned_data['text'])
            post.save()
            page = (thread.post_count()/request.user.profile.ppp)+1
            return HttpResponseRedirect(reverse('thread-page_view', args=(thread.id,page)))
        else:
            posts_per_page = request.user.profile.ppp

    pages = Paginator(thread.post_set.all().order_by('pk'), posts_per_page)
    try:
        posts = pages.page(page)
    except PageNotAnInteger:
        posts = pages.page(1)
    except EmptyPage:
        posts = pages.page(pages.num_pages)
    return render_to_response('forums/thread.html',{'thread':thread, 'posts':posts, 'form': form}, context_instance=RequestContext(request))
          

def single_post(request, post):
    post = get_object_or_404(Post, pk=post)
    return render_to_response('forums/post.html',{'post':post}, context_instance=RequestContext(request))

def vote(request, poll):
    poll = get_object_or_404(Poll, pk=poll)
    user = request.user
    if not user.is_authenticated():
        # Should not be possible, an error in the template...
        return HttpResponseRedirect(reverse('forums.views.show_thread', args=(poll.thread.id,1)))
    try:
        selected_choice = poll.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return HttpResponseRedirect(reverse('forums.views.show_thread', args=(poll.thread.id,1)))
    new_vote = PollVote(user=user, vote=selected_choice)
    return HttpResponseRedirect(reverse('forums.views.show_thread', args=(poll.thread.id,1)))

def post_thread(request, board):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login/?next=%s' % request.path)
    board = get_object_or_404(Category, pk=board)
    if not (board in request.user.profile.group.allowed_post.all()):
        return HttpResponseRedirect(reverse('board_view', args=(board.id,)))
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['category_id'] != board.id:
                raise PermissionDenied
            thread = Thread(creator = request.user, category = board, subject = form.cleaned_data['subject'])
            thread.save()
            post = Post(user = request.user, thread = thread, text = form.cleaned_data['text'])
            post.save()
            return HttpResponseRedirect(reverse('thread-page_view', args=(thread.id,1)))
    else:
        form = ThreadForm({'category_id':board.id})
    return render_to_response('forums/post_thread.html',{'form':form,'board':board}, context_instance=RequestContext(request))


def edit_post(request, post):
    post = get_object_or_404(Post, pk=post)
    user = request.user
    if not (user.is_authenticated() and (user==post.user or user.has_perm('forums.can_moderate') or user.is_superuser)):
        raise PermissionDenied
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['thread_id'] != post.thread.id or form.cleaned_data['post_id'] != post.id:
                raise PermissionDenied
            post.text = form.cleaned_data['text']
            post.save()
            return HttpResponseRedirect(reverse('thread-page_view', args=(post.thread.id,1)))
    else:
        form = PostForm({'text': post.text, 'thread_id': post.thread.id, 'post_id': post.id})
    return render_to_response('forums/edit_post.html',{'form':form,'post':post}, context_instance=RequestContext(request))
