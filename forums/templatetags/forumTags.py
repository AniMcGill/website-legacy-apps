from django import template


register = template.Library()

@register.simple_tag(takes_context=True)
def readTrackIMG(context,thread,read,unread):
    user = context['user']
    if user.is_authenticated():
        tracker = thread.getReadTracker(user)
        if tracker.unread():
            img = "<img src=\""+unread+"\" alt=\"unread\" \\>"
        else:
            img = "<img src=\""+read+"\" alt=\"read\" \\>"
    else:
        img = "<img src=\""+read+"\" alt=\"read\" \\>"
    return img

@register.simple_tag(takes_context=True)
def readBoardIMG(context,board,read,unread):
    user = context['user']
    if user.is_authenticated():
        tracker = board.getReadTracker(user)
        if tracker.unread():
            img = "<img src=\""+unread+"\" alt=\"unread\" \\>"
        else:
            img = "<img src=\""+read+"\" alt=\"read\" \\>"
    else:
        img = "<img src=\""+read+"\" alt=\"read\" \\>"
    return img
