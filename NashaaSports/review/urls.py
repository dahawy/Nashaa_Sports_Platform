from django.urls import path
from . import views

app_name = "review"

urlpatterns = [
    path("reviews/add/<program_id>/", views.add_review_view, name="add_review_view"),
]

    # path("reviews/delete/<review_id>/", views.delete_review_view, name="delete_review_view"),
    # path("bookmarks/add/<game_id>/", views.add_bookmark_view, name="add_bookmark_view")