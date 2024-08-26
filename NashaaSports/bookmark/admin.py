from django.contrib import admin
from .models import ProgramBookmark



class ProgramBookmarkAdmin(admin.ModelAdmin):

    list_display=("id","user_id", "program_id","created_at")

# Unregister the default User admin and register the customized one
admin.site.register(ProgramBookmark, ProgramBookmarkAdmin)
