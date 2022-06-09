"""
Serializers for the user API View
"""
from django.contrib.auth import get_user_model

# Serializers convert JSON to python obj or models in the db
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    # Tell django the model and the fields to pass to the serializer
    class Meta:
        model = get_user_model()
        # Remove is_staff or is_active: admin responsability
        fields = ['email', 'password', 'name']
        # Will not return the password in the response
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    # Set encryption, by overrinding the creation method
    # Call after the validation, only if it's successfull
    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)
