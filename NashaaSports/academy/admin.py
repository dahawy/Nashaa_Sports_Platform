from django.contrib import admin
from academy.models import Branch
from academy.models import Coach
from academy.models import TimeSlot
from academy.models import ProgramImage
from academy.models import ProgramVideo
from academy.models import Program

class ProgramAdmin(admin.ModelAdmin):
    list_display = ('id', 'branch', 'program_name', 'description', 'fees', 'start_date','end_date','min_age','max_age','sport_category','is_available','registration_end_date','is_active')



admin.site.register(Program,ProgramAdmin)
admin.site.register(Branch)
admin.site.register(Coach)
admin.site.register(TimeSlot)
admin.site.register(ProgramImage)
admin.site.register(ProgramVideo)
