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
    path("admin/", include("admin.urls")),
    
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
