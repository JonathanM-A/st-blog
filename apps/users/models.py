import uuid
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from ..common.models import BaseModel


class UserManager(BaseUserManager):
    def create_user(
        self,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        **extra_fields,
    ):
        if not all([email, password, first_name, last_name]):
            raise ValueError("All fields are required.")

        try:
            validate_password(password)
        except ValidationError as e:
            raise ValidationError(f"password: {e.messages}")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )
        user.set_password(password)
        user.full_clean()
        user.save()

        return user

    def create_superuser(
        self,
        email: str,
        password: str,
        first_name: str = "Admin",
        last_name: str = "User",
        **extra_fields,
    ):

        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )

        user.set_password(password)
        user.save()

        if not user.is_superuser:
            raise ValueError("Superuser must have is_superuser=True.")

        return user
    

class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
