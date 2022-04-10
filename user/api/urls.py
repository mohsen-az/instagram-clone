from django.urls import path

from relation.api.views import FollowerListAPIView, FollowingListAPIView, InvitationListAPIView
from user.api import views


urlpatterns = [
    path("profile/invitation/", InvitationListAPIView.as_view()),
    path("profile/follower/", FollowerListAPIView.as_view()),
    path("profile/following/", FollowingListAPIView.as_view()),
    path("profile/<str:username>/", views.ProfileRetrieveAPIView.as_view()),
    path("profile/", views.ProfileRetrieveUpdateAPIView.as_view()),
]
