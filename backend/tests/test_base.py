"""
Tests base para el proyecto.
"""
import pytest
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status


class BaseTestCase(TestCase):
    """
    Clase base para tests del proyecto.
    """
    
    def setUp(self):
        """
        Configuración base para tests.
        """
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )


class BaseAPITestCase(APITestCase):
    """
    Clase base para tests de API.
    """
    
    def setUp(self):
        """
        Configuración base para tests de API.
        """
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def authenticate_user(self):
        """
        Autentica el usuario para las pruebas.
        """
        self.client.force_authenticate(user=self.user)
        
    def test_health_check(self):
        """
        Test del endpoint de health check.
        """
        response = self.client.get('/health/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('status', response.data)
        self.assertEqual(response.data['status'], 'healthy')
