from rest_framework import serializers
from .models import User
from rest_framework.exceptions import ValidationError
from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from allauth.account.models import EmailAddress

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'password']
        read_only_fields = ['id']


class CustomRegisterSerializer(RegisterSerializer):
    username = None  # Disable username field
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    def validate_email(self, email):
        """
        Checks if the email already exists in the EmailAddress model.
        This prevents creating a new user if an unverified email already exists,
        avoiding a database IntegrityError (500).
        """
        email = get_adapter().clean_email(email)

        # Check for existence of the email, regardless of verified status
        if EmailAddress.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError(
                ("A user is already registered with this e-mail address.")
            )
        return email

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data.update(
            {
                "first_name": self.validated_data.get("first_name", ""),  # type: ignore
                "last_name": self.validated_data.get("last_name", ""),  # type: ignore
            }
        )
        return data

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()

        # Save all fields to the user instance
        for key, value in self.cleaned_data.items():
            setattr(user, key, value)

        adapter.save_user(request, user, self, commit=False)

        # Perform password validation
        if "password1" in self.cleaned_data:
            try:
                adapter.clean_password(self.cleaned_data["password1"], user=user)
            except ValidationError as exc:
                raise serializers.ValidationError(
                    detail=serializers.as_serializer_error(exc)
                )

        user.save()
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user
