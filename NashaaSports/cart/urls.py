from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("cart/summary/<int:cart_id>/", views.cart_summary_view, name="cart_summary_view" ),
]