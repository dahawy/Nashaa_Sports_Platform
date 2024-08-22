from django.urls import path
from . import views

app_name = "moderator"

urlpatterns = [
    path('moderator_dashboard/',views.moderator_dashboard_view,name="moderator_dashboard_view"),
    path('customers_queries/<status>/',views.customers_queries_view, name='customers_queries_view'),
    path('academies_for_approval/',views.academies_for_approval_view, name='academies_for_approval_view'),
    path('academy_detail/<academy_id>/',views.academy_detail_view, name='academy_detail_view'),
    path('approve_academy/<academy_id>/',views.approve_academy_view, name='approve_academy_view'),
    path('approved_academies/',views.approved_academies_view, name='approved_academies_view'),
    path('users/<user_type>',views.users_view, name='users_view'),
    path('programs/<academy_id>',views.programs_view, name='programs_view'),
    path('deactivate_program/<academy_id>',views.deactivate_program_view, name='deactivate_program_view'),
    path('query_detail/<query_id>/', views.query_detail_view, name='query_detail_view'),
]







