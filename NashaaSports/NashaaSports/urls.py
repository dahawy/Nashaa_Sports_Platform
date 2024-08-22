"""
URL configuration for NashaaSports project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path ,include
from django.conf.urls.static import static
from . import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("main.urls")),
    path("account/", include("account.urls")),
    path("academy/", include("academy.urls")),
    path("bookmark/", include("bookmark.urls")),
    path("cart/", include("cart.urls")),
    path("client/", include("client.urls")),
    path("contactUs/", include("contactUs.urls")),
    path("enrollment/", include("enrollment.urls")),
    path("review/", include("review.urls")),
    path("moderator/", include("moderator.urls")),
    path("payment/", include("payment.urls")),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='reset_password.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='reset_password_done.html'), name='password_reset_done'),
    path('reset/confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name="password_reset_confirm"),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
