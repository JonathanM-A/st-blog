from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserSerializer, CustomRegisterSerializer
from dj_rest_auth.registration.views import RegisterView


class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer


class UserDetailView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.none()
    serializer_class = UserSerializer

    def get_object(self): # type: ignore
        return self.request.user
    