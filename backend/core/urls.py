"""
URLs del módulo core.
"""
from django.urls import path
from .views import (
    HealthCheckView,
    CustomAuthToken,
    LogoutView,
    UserProfileView,
    RegisterView
)

app_name = 'core'

urlpatterns = [
    path('', HealthCheckView.as_view(), name='health-check'),
    # Endpoints de autenticación
    path('auth/login/', CustomAuthToken.as_view(), name='auth-login'),
    path('auth/logout/', LogoutView.as_view(), name='auth-logout'),
    path('auth/register/', RegisterView.as_view(), name='auth-register'),
    path('auth/profile/', UserProfileView.as_view(), name='auth-profile'),
]
