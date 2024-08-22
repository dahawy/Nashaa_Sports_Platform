from django.urls import path
from . import views

app_name = "payment"

urlpatterns = [
    path("cart/payment/<int:cart_id>/", views.process_payment, name="process_payment"),
]