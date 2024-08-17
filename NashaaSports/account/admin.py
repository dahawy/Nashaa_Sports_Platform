from django.contrib import admin
from .models import UserProfile
from .models import AcademyProfile


class ProfileAdmin(admin.ModelAdmin):
    list_display=("name","nationality","gender","id_number")

class ProfileAcademy(admin.ModelAdmin):
    list_display=("academy_name", "description", "approved", "logo", "created_at")


admin.site.register(UserProfile,ProfileAdmin)
admin.site.register(AcademyProfile,ProfileAcademy)