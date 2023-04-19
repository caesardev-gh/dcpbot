from django.contrib import admin
from django.contrib.auth.models import User as DefaultUser, Group

from .models import *

admin.site.unregister(DefaultUser)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ('user_id', 'username', 'first_name', 'last_name', 'joined_at', 'last_seen',)
    readonly_fields = ('user_id', 'username', 'joined_at', 'last_seen')
    list_display = ('user_id', 'username', 'first_name', 'last_name', 'joined_at', 'last_seen',)

    def has_add_permission(self, request):
        return False


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    fields = ('id', 'role', 'chat_id', 'user', 'text', 'date',)
    readonly_fields = ('id', 'date',)
    list_display = ('id', 'role', 'chat_id', 'user', 'text', 'date',)
