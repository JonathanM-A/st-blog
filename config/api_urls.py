from django.urls import path, include

urlpatterns = [
    path("posts/", include("apps.posts.urls", namespace="posts")),
    path("users/", include("apps.users.urls", namespace="users")),
]