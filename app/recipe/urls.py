"""
URL mapping for the recipe app.
"""

from django.urls import (path, include)
from rest_framework.routers import DefaultRouter
from recipe import views

# Set all CRUD operations automatically by the DefaultRouter
router = DefaultRouter()
router.register('recipes', views.RecipeViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
]
