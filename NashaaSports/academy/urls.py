from django.urls import path
from . import views

app_name = "academy"

urlpatterns = [
    path('add/branch/<int:user_id>/',views.add_branch_view,name="add_branch_view"),
    path('dashboard/<user_id>/',views.acadmey_dashboard_view,name="academy_dashboard_view"),
    path('add/program/<user_id>/',views.add_program_view,name="add_program_view"),
    path('add/coach/<user_id>/',views.add_coach_view,name="add_coach_view")
]
