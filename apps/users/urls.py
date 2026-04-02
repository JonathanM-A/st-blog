from django.urls import path
from .views import UserDetailView

app_name = "users"

urlpatterns = [
    path("profile/", UserDetailView.as_view(), name="profile"),
]