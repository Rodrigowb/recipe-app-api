from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)

# Creating user manager


class UserManager(BaseUserManager):
    """Manager for users"""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user"""
        # Define a new user
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        # Support multiple dbs to the same project (edge case...)
        user.save(using=self._db)

        return user


# Creating user model
# AbstractBaseUser contains the functionalities for authentication
# PermissionsMixin contains the functionalities permissions


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Assign a user manager
    objects = UserManager()

    # Defines the field we wanna use for authentication
    USERNAME_FIELD = 'email'
