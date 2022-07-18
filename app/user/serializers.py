"""
Serializers for the user API View
"""
from django.contrib.auth import (get_user_model, authenticate)
from django.utils.translation import gettext as _

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


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')
        # Built in django auth function
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
