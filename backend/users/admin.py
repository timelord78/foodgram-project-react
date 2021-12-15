from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import MyUser


class MyUserAdmin(BaseUserAdmin):
    list_display = ('pk', 'username', 'email')
    list_filter = BaseUserAdmin.list_filter + ('email', 'username')


admin.site.register(MyUser, MyUserAdmin)
