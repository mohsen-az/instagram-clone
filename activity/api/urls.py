from django.urls import path

from activity.api import views

app_name = "api-activity"

urlpatterns = [
    path("comments/<int:pk>/add/", views.CommentCreateAPIView.as_view(), name="create-comment"),
    path("likes/<int:pk>/like/", views.LikeAPIView.as_view(), name="like"),
    path("likes/<int:pk>/unlike/", views.UnLikeAPIView.as_view(), name="unlike"),
]
