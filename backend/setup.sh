#!/bin/bash
# Script para configuración inicial del proyecto

echo "🚀 Configurando Smart Drawers Backend..."

# Verificar que estamos en el directorio correcto
if [ ! -f "manage.py" ]; then
    echo "❌ Error: No se encontró manage.py. Asegúrate de estar en el directorio backend."
    exit 1
fi

# Activar entorno virtual
echo "📦 Activando entorno virtual..."
if [ -d ".venv" ]; then
    source .venv/bin/activate  # Linux/Mac
    # .venv\Scripts\activate.bat  # Windows
else
    echo "⚠️  Entorno virtual no encontrado. Creando..."
    python -m venv .venv
    source .venv/bin/activate  # Linux/Mac
fi

# Instalar dependencias
echo "📚 Instalando dependencias..."
pip install -r requirements/development.txt

# Crear archivo .env si no existe
if [ ! -f ".env" ]; then
    echo "⚙️  Creando archivo .env..."
    cp .env.example .env
    echo "📝 Por favor, edita el archivo .env con tus configuraciones."
fi

# Verificar configuración
echo "🔍 Verificando configuración de Django..."
python manage.py check

echo "✅ Configuración inicial completada!"
echo ""
echo "📋 Próximos pasos:"
echo "1. Editar el archivo .env con tus configuraciones de base de datos"
echo "2. Crear la base de datos MySQL"
echo "3. Ejecutar: python manage.py migrate"
echo "4. Ejecutar: python manage.py createsuperuser"
echo "5. Ejecutar: python manage.py runserver"
echo ""
echo "🌐 Health check disponible en: http://localhost:8000/health/"
