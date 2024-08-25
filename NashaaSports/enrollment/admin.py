from django.contrib import admin
from enrollment.models import Enrollment
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'program', 'cart','time_slot', 'first_name', 'father_name', 'last_name','health_condition','id_number','created_at')



admin.site.register(Enrollment,ProgramAdmin)

