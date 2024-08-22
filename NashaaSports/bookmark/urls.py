from django.urls import path
from . import views

app_name = "bookmark"

urlpatterns = [
    path("bookmark/add/<program_id>/", views.add_bookmark_view, name="add_bookmark_view")
]