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
        # Make all users has email
        if not email:
            raise ValueError('Users must have an email address.')
        # Define a new user
        # Including email normalized method (provided by the base user manager)
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        # Support multiple dbs to the same project (edge case...)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
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
