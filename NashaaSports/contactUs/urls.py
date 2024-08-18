from django.urls import path
from . import views

app_name = "contactUs"

urlpatterns = [
    path('customer_query/',views.customer_query_view, name='customer_query_view'),
]