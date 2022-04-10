from django.urls import path, include

from rest_framework.routers import SimpleRouter

from content.api import views

post_router = SimpleRouter()
post_router.register(prefix='posts', viewset=views.PostReadOnlyModelViewSet)

urlpatterns = [
    path("<str:username>/", include(post_router.urls)),
    path("post/add/", views.PostCreateAPIView.as_view())
]
