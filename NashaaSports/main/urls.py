from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.home_view, name="home_view"),
    path("programs/",views.programs_view,name="programs_view"),
    path("program/detail/<program_id>", views.program_detail_view, name="program_detail_view"),

]