"""
Tests para el módulo core.
"""
from django.test import TestCase
from django.contrib.auth.models import User
from core.models import BaseModel, AuditableModel
from tests.test_base import BaseAPITestCase


class TestCoreModels(TestCase):
    """
    Tests para los modelos del core.
    """
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_base_model_creation(self):
        """
        Test de creación de modelo base.
        Como BaseModel es abstracto, no podemos crear instancias directamente.
        Este test verifica que los campos estén definidos correctamente.
        """
        # Verificar que los campos están definidos en BaseModel
        self.assertTrue(hasattr(BaseModel, 'id'))
        self.assertTrue(hasattr(BaseModel, 'created_at'))
        self.assertTrue(hasattr(BaseModel, 'updated_at'))
        self.assertTrue(hasattr(BaseModel, 'is_active'))


class TestCoreViews(BaseAPITestCase):
    """
    Tests para las views del core.
    """
    
    def test_health_check_endpoint(self):
        """
        Test del endpoint de health check.
        """
        response = self.client.get('/health/')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('status', response.data)
        self.assertEqual(response.data['status'], 'healthy')
        self.assertIn('message', response.data)
        self.assertIn('version', response.data)
