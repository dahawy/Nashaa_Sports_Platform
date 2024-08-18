from django.urls import path
from . import views

app_name = "academy"

urlpatterns = [
    path("add/program/time/<program_id>",views.add_program_time_slot_view,name="add_program_time_slot_view"),
    path("delete/time/slot/<time_slot_id>",views.delete_time_slot_view,name="delete_time_slot_view"),
    path('add/branch/<int:user_id>/',views.add_branch_view,name="add_branch_view"),
    path('dashboard/<user_id>/',views.acadmey_dashboard_view,name="academy_dashboard_view"),
    path('add/program/<user_id>/',views.add_program_view,name="add_program_view"),
    path('add/coach/<user_id>/',views.add_coach_view,name="add_coach_view"),
    path('add/program/media/<program_id>',views.upload_media_view,name="upload_media_view"),


]
