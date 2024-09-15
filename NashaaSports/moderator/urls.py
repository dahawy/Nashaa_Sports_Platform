from django.urls import path
from . import views

app_name = "moderator"

urlpatterns = [
    path('moderator_dashboard/<int:days_ago>/',views.moderator_dashboard_view,name="moderator_dashboard_view"),
    path('customers_queries/<status>/',views.customers_queries_view, name='customers_queries_view'),
    path('academies_for_approval/',views.academies_for_approval_view, name='academies_for_approval_view'),
    path('academy_detail/<academy_id>/',views.academy_detail_view, name='academy_detail_view'),
    path('approve_academy/<academy_id>/',views.approve_academy_view, name='approve_academy_view'),
    path('disapprove_academy/<academy_id>/',views.disapprove_academy_view, name='disapprove_academy_view'),
    path('approved_academies/',views.approved_academies_view, name='approved_academies_view'),
    path('users/<user_type>',views.users_view, name='users_view'),
    path('programs/<academy_id>',views.programs_view, name='programs_view'),
    path('deactivate_program/<academy_id>',views.deactivate_program_view, name='deactivate_program_view'),
    path('query_detail/<query_id>/', views.query_detail_view, name='query_detail_view'),
    path('subscribers/', views.subscribers_view, name='subscribers_view'),
    path('academy_branches/<academy_id>',views.academy_branches_view,name="academy_branches_view"),
    path('branch/delete/<branch_id>',views.delete_branch_view,name="delete_branch_view"),
    path('branch/update/<branch_id>',views.update_branch_view,name="update_branch_view"),
    path('coaches/<academy_id>',views.coaches_view,name="coaches_view"),
    path('coach/delete/<coach_id>',views.delete_coach_view,name="delete_coach_view"),
    path('coach/update/<coach_id>',views.update_coach_view,name="update_coach_view"),
]







