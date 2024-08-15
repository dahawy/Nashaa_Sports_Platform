from django.contrib import admin
from .models import UserProfile


class ProfileAdmin(admin.ModelAdmin):
    list_display=("name","nationality","gender","id_number")


admin.site.register(UserProfile,ProfileAdmin)