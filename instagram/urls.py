"""instagram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from user import views

urlpatterns = [
    path('admin/', admin.site.urls),
]

# Client Side Rendering
urlpatterns += [
    # Authentication API
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Include Apps
    path("api/auth/", include("user.api.urls")),
    path("api/content/", include("content.api.urls")),
    path("api/activity/", include("activity.api.urls")),
    path("api/relation/", include("relation.api.urls")),
]

# Server Side Rendering
urlpatterns += [
    # Include Apps
    path("auth/", include("user.urls", namespace="user")),
    path("relation/", include("relation.urls", namespace="relation")),

    # Render Simple Page
    path("", TemplateView.as_view(template_name="user/home.html"), name="home"),

    # Other route
    path("<str:username>/", views.ProfileDetailView.as_view(), name="profile"),
    path("<str:username>/following/", views.FollowingListView.as_view(), name="following"),
    path("<str:username>/follower/", views.FollowerListView.as_view(), name="follower"),
    path("<str:username>/invitation/", views.InvitationListView.as_view(), name="invitation"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
