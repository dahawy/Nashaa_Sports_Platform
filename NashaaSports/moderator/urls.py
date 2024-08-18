from django.urls import path
from . import views

app_name = "moderator"

urlpatterns = [
    path('customers_queries/',views.customers_queries_view, name='customers_queries_view'),
    path('query_detail/<query_id>/', views.query_detail_view, name='query_detail_view'),
]







