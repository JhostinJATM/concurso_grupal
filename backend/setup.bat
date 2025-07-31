@echo off
REM Script para configuración inicial del proyecto en Windows

echo 🚀 Configurando Smart Drawers Backend...

REM Verificar que estamos en el directorio correcto
if not exist "manage.py" (
    echo ❌ Error: No se encontró manage.py. Asegúrate de estar en el directorio backend.
    pause
    exit /b 1
)

REM Activar entorno virtual
echo 📦 Activando entorno virtual...
if exist ".venv" (
    call .venv\Scripts\activate.bat
) else (
    echo ⚠️  Entorno virtual no encontrado. Creando...
    python -m venv .venv
    call .venv\Scripts\activate.bat
)

REM Instalar dependencias
echo 📚 Instalando dependencias...
pip install -r requirements\development.txt

REM Crear archivo .env si no existe
if not exist ".env" (
    echo ⚙️  Creando archivo .env...
    copy .env.example .env
    echo 📝 Por favor, edita el archivo .env con tus configuraciones.
)

REM Verificar configuración
echo 🔍 Verificando configuración de Django...
python manage.py check

echo ✅ Configuración inicial completada!
echo.
echo 📋 Próximos pasos:
echo 1. Editar el archivo .env con tus configuraciones de base de datos
echo 2. Crear la base de datos MySQL
echo 3. Ejecutar: python manage.py migrate
echo 4. Ejecutar: python manage.py createsuperuser
echo 5. Ejecutar: python manage.py runserver
echo.
echo 🌐 Health check disponible en: http://localhost:8000/health/

pause
