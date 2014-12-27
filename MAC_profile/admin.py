from django.contrib import admin
from MAC_profile.models import Profile, Exec

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_name', 'user', 'website_text', 'gender', 'group')
    search_fields = ['id', 'display_name', 'user__email', 'user__username']

class ExecAdmin(admin.ModelAdmin):
    list_display = ('user', 'position', 'active')
    list_filter = ('active', 'position')
    search_fields = [ 'user.username', 'position']
    exclude = ('about_saved',)

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Exec, ExecAdmin)
