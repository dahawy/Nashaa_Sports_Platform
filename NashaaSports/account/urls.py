from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path('signup/', views.sign_up, name="sign_up"),
    path('signup/as/academy', views.sing_up_asAcademy_view, name="sing_up_asAcademy_view"),
    path('my/academy/profile/<user_name>', views.academy_profile_view, name="academy_profile_view"),
    path('create/academy/profile/<user_name>', views.create_academy_profile_view, name="create_academy_profile_view"),
    path('login/', views.log_in, name="log_in"),
    path('logout/', views.log_out, name="log_out"),
    path('profile/<user_name>/',views.profile_view, name="profile_view"),
    path('addProfile/<user_name>/',views.create_profile_view, name="create_profile_view")
]