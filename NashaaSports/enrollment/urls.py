from django.urls import path
from . import views

app_name = "enrollment"

urlpatterns = [

    path("enroll/<int:program_id>/<int:user_id>", views.enroll_in_program_view, name="enroll_in_program_view"),
    # path("add/enrollment/", views.add_enrollment_view, name="add_enrollment_view"),
    path("my/enrollment/<int:user_id>", views.my_enrollment_view, name="my_enrollment_view"),
    path('pending/status/<enrollment_id>',views.pending_enrollment_status_view,name="pending_enrollment_status_view"),
    path('in_progress/status/<enrollment_id>',views.in_progress_enrollment_status_view,name="in_progress_enrollment_status_view"),
    
]