from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Post
from .serializers import PostSerializer


class PostViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.none()
    serializer_class = PostSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    search_fields = ['title', 'content']

    def get_queryset(self): # type: ignore
        user = self.request.user
        if not user.is_authenticated:
            return Post.objects.none()
        
        base_queryset = (
            Post.objects.all() if user.is_superuser
            else Post.objects.filter(author=user, is_active=True)
        )
        
        return base_queryset.select_related('author').order_by('-created_at')
