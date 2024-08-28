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
    path("program/detail/<program_id>",views.program_detail_view,name="program_detail_view"),
    path('profile/<academy_id>',views.academies_profile_view,name="academies_profile_view"),
    path('programs/list',views.programs_list_view,name="programs_list_view"),
    path('program/delete/<program_id>',views.delete_program_view,name='delete_program_view'),
    path('update/program/<program_id>',views.update_programs_info_view,name="update_programs_info_view"),
    path('update/time-slot/<program_id>',views.update_time_slot_view,name='update_time_slot_view'),
    path('update/media/<program_id>',views.update_media_view,name="update_media_view"),
    path('branches/<user_id>',views.branches_list_view,name="branches_list_view"),
    path('branch/delete/<branch_id>',views.delete_branch_view,name="delete_branch_view"),
    path('branch/update/<branch_id>',views.update_branch_view,name="update_branch_view"),
    path('coaches/list/<academy_id>',views.coach_list_view,name="coach_list_view"),
    path('coach/delete/<coach_id>',views.delete_coach_view,name="delete_coach_view"),
    path('coach/update/<coach_id>',views.update_coach_view,name="update_coach_view"),
    path('subscribers/<user_id>',views.subscribers_view,name="subscribers_view"),
    path('image/delete/<image_id>/',views.delete_image,name="delete_image"),
    path('video/delete/<video_id>/',views.delete_video,name="delete_video"),
    path('more/programs/<academy_id>',views.more_programs_view,name='more_programs_view'),
   
    
]
