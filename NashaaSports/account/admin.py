from django.contrib import admin
from .models import UserProfile
from .models import AcademyProfile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin



class ProfileAdmin(admin.ModelAdmin):

    list_display=("id","user_id", "name","nationality","gender","id_number")


class ProfileAcademy(admin.ModelAdmin):
    list_display=("id","academy_name", "description", "approved", "logo", "created_at")

class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile,ProfileAdmin)
admin.site.register(AcademyProfile,ProfileAcademy)


class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff')

# Unregister the default User admin and register the customized one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
