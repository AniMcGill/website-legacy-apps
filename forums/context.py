from forums.models import *

def category_processor(request):
    if request.user.is_authenticated():
        cats = request.user.profile.group.allowed_read.filter(parent = None)
    else:
        cats = Category.objects.filter( anon_viewable = True ).filter( parent = None )
    return {'categories': cats}
