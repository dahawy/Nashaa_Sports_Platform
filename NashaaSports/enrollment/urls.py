from django.urls import path
from . import views

app_name = "enrollment"

urlpatterns = [

    path("enroll/<int:program_id>/<int:user_id>", views.enroll_in_program_view, name="enroll_in_program_view"),
    path("add/enrollment/", views.add_enrollment_view, name="add_enrollment_view"),
    
]