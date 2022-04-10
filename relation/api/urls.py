from django.urls import path

from relation.api import views

urlpatterns = [
    path("friendships/<int:pk>/follow/", views.FollowAPIView.as_view()),
    path("friendships/<int:pk>/unfollow/", views.UnFollowAPIView.as_view()),
    path("friendships/<int:pk>/accept/", views.AcceptInvitationAPIView.as_view()),
    path("friendships/<int:pk>/reject/", views.RejectInvitationAPIView.as_view()),
]
