from forums.models import *
from django.contrib import admin

class ThreadAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('subject','creator','created','last','category','has_poll','post_count',)
    list_filter = ('category',)
    search_fields = ['=creator', 'subject']
    fieldsets = (
        (None, { 'fields': ('subject','category','creator','locked','sticky')}),
    )
    

admin.site.register(Category)
admin.site.register(Thread,ThreadAdmin)
admin.site.register(Post)
admin.site.register(Poll)
admin.site.register(Attachment)
