from django.urls import path
from . import views

app_name = "enrollment"

urlpatterns = [
    path("enroll/<int:user_id>/<int:program_id>/", views.enroll_in_program_view, name="enroll_in_program_view"),
    
]