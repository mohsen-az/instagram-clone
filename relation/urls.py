from django.urls import path

from relation import views

app_name = "relation"

urlpatterns = [
    path("<str:username>/follow/", views.FollowView.as_view(), name="follow"),
    path("<str:username>/unfollow/", views.UnFollowView.as_view(), name="unfollow"),
    path("<str:username>/accept/", views.AcceptInvitationView.as_view(), name="accept-invitation"),
    path("<str:username>/reject/", views.RejectInvitationView.as_view(), name="reject-invitation"),
]
