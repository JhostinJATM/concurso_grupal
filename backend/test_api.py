#!/usr/bin/env python
"""
Script para probar las APIs de autenticación y cajones.
"""
import os
import sys
import django
import requests
import json

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

def test_api():
    base_url = "http://localhost:8000/api/v1"
    
    # 1. Crear usuario de prueba si no existe
    print("1. Creando usuario de prueba...")
    username = "test_user"
    password = "test123456"
    
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    
    if created:
        user.set_password(password)
        user.save()
        print(f"Usuario '{username}' creado exitosamente")
    else:
        print(f"Usuario '{username}' ya existe")
    
    # 2. Obtener token
    print("\n2. Obteniendo token de autenticación...")
    login_data = {
        "username": username,
        "password": password
    }
    
    response = requests.post(f"{base_url}/auth/login/", json=login_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        token_data = response.json()
        token = token_data.get('token')
        print(f"Token obtenido: {token[:20]}...")
        
        # Headers para requests autenticados
        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': 'application/json'
        }
        
        # 3. Listar cajones existentes
        print("\n3. Listando cajones existentes...")
        response = requests.get(f"{base_url}/cajones/", headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        # 4. Crear nuevo cajón
        print("\n4. Creando nuevo cajón...")
        cajon_data = {
            "nombre": "Cajon de Prueba",
            "capacidad_maxima": 15,
            "descripcion": "Este es un cajon de prueba creado via API"
        }
        
        response = requests.post(f"{base_url}/cajones/", json=cajon_data, headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            cajon_creado = response.json()
            cajon_id = cajon_creado.get('id')
            print(f"Cajón creado exitosamente con ID: {cajon_id}")
            
            # 5. Crear objeto en el cajón
            print("\n5. Creando objeto en el cajón...")
            objeto_data = {
                "nombre": "Objeto de Prueba",
                "tipo_objeto": "ELECTRONICA",
                "tamanio": "MEDIANO",
                "cajon": cajon_id,
                "descripcion": "Este es un objeto de prueba"
            }
            
            response = requests.post(f"{base_url}/objetos/", json=objeto_data, headers=headers)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            
        else:
            print("Error al crear cajón")
    else:
        print("Error al obtener token")

if __name__ == "__main__":
    test_api()
