"""
URL mappings for the user API
"""
from django.urls import path
from user import views

# Used by the reverse function in the test_user_api
app_name = 'user'

# Defines the url to be handled by requests
urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token')
]
