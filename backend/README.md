# Smart Drawers Backend

Backend para el sistema de simulación de comportamiento inteligente de cajones, desarrollado con Django REST Framework siguiendo principios de Clean Architecture, SOLID y buenas prácticas de desarrollo.

## 🏗️ Arquitectura

El proyecto sigue una arquitectura limpia y modular:

```
backend/
├── apps/                   # Aplicaciones del dominio
├── config/                 # Configuración del proyecto
│   ├── settings/          # Configuraciones por ambiente
│   │   ├── base.py        # Configuración base
│   │   ├── development.py # Configuración de desarrollo
│   │   ├── production.py  # Configuración de producción
│   │   └── testing.py     # Configuración para tests
│   ├── urls.py            # URLs principales
│   ├── wsgi.py            # WSGI application
│   └── asgi.py            # ASGI application
├── core/                   # Funcionalidades base
│   ├── models.py          # Modelos base abstractos
│   ├── views.py           # Views base
│   ├── serializers.py     # Serializadores base
│   └── urls.py            # URLs del core
├── utils/                  # Utilidades comunes
│   ├── exceptions.py      # Excepciones personalizadas
│   ├── validators.py      # Validadores
│   └── helpers.py         # Funciones de ayuda
├── requirements/           # Dependencias por ambiente
├── static/                # Archivos estáticos
├── media/                 # Archivos multimedia
├── templates/             # Templates
├── tests/                 # Tests del proyecto
└── logs/                  # Archivos de log
```

## 🚀 Características

-   **Clean Architecture**: Separación clara de responsabilidades
-   **Principios SOLID**: Código mantenible y extensible
-   **Django REST Framework**: API REST robusta
-   **Base de datos MySQL**: Configurada para MySQL
-   **Configuración modular**: Diferentes configuraciones por ambiente
-   **Sistema de logging**: Logging estructurado
-   **Tests**: Configuración completa para testing
-   **Validaciones personalizadas**: Sistema robusto de validación
-   **Manejo de excepciones**: Sistema centralizado de manejo de errores

## 📋 Prerrequisitos

-   Python 3.11+
-   MySQL 8.0+
-   pip
-   virtualenv (recomendado)

## 🛠️ Instalación

1. **Clonar el repositorio**

    ```bash
    git clone <repository-url>
    cd backend
    ```

2. **Crear y activar entorno virtual**

    ```bash
    python -m venv .venv
    .venv\Scripts\activate  # En Windows
    source .venv/bin/activate  # En Linux/Mac
    ```

3. **Instalar dependencias**

    ```bash
    pip install -r requirements/development.txt
    ```

4. **Configurar variables de entorno**

    ```bash
    cp .env.example .env
    # Editar .env con tus configuraciones
    ```

5. **Configurar base de datos MySQL**

    - Crear la base de datos en MySQL
    - Actualizar las credenciales en el archivo `.env`

6. **Ejecutar migraciones**

    ```bash
    python manage.py migrate
    ```

7. **Crear superusuario**

    ```bash
    python manage.py createsuperuser
    ```

8. **Ejecutar servidor de desarrollo**
    ```bash
    python manage.py runserver
    ```

## 📊 Base de Datos

El proyecto está configurado para usar MySQL como base de datos principal. La configuración se encuentra en `config/settings/base.py` y utiliza las siguientes variables de entorno:

-   `DB_NAME`: Nombre de la base de datos
-   `DB_USER`: Usuario de MySQL
-   `DB_PASSWORD`: Contraseña de MySQL
-   `DB_HOST`: Host de MySQL (default: localhost)
-   `DB_PORT`: Puerto de MySQL (default: 3306)

## 🧪 Testing

Ejecutar todos los tests:

```bash
pytest
```

Ejecutar tests con coverage:

```bash
pytest --cov=.
```

Ejecutar tests específicos:

```bash
pytest tests/test_core.py
```

## 📝 Desarrollo

### Crear nueva aplicación

```bash
cd apps
python ../manage.py startapp nombre_app
```

### Estructura de una aplicación

Cada aplicación debe seguir la siguiente estructura:

```
app_name/
├── models.py          # Modelos del dominio
├── views.py           # Views/Controllers
├── serializers.py     # Serializadores DRF
├── urls.py            # URLs de la app
├── admin.py           # Configuración del admin
├── tests/             # Tests de la aplicación
│   ├── test_models.py
│   ├── test_views.py
│   └── test_serializers.py
└── migrations/        # Migraciones de BD
```

### Code Quality

El proyecto incluye herramientas para mantener la calidad del código:

```bash
# Formatear código
black .
isort .

# Verificar estilo
flake8

# Type checking
mypy .
```

## 🌍 Ambientes

### Desarrollo

```bash
export DJANGO_ENVIRONMENT=development
python manage.py runserver
```

### Producción

```bash
export DJANGO_ENVIRONMENT=production
python manage.py runserver
```

### Testing

```bash
export DJANGO_ENVIRONMENT=testing
pytest
```

## 📡 API Endpoints

### Health Check

-   `GET /health/` - Verificar estado de la API

### Admin

-   `GET /admin/` - Panel de administración Django

### API REST

-   `GET/POST /api/v1/` - Endpoints de la API (se expandirán con las aplicaciones)

## 🔧 Configuración

### Variables de Entorno

Crear un archivo `.env` basado en `.env.example` con las siguientes variables:

```env
# Django
SECRET_KEY=your-secret-key
DEBUG=True
DJANGO_ENVIRONMENT=development
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=smart_drawers_dev
DB_USER=root
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=3306

# Email (opcional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## 📚 Principios Aplicados

### SOLID

-   **S**: Single Responsibility - Cada clase tiene una responsabilidad específica
-   **O**: Open/Closed - Abierto para extensión, cerrado para modificación
-   **L**: Liskov Substitution - Las subclases deben ser sustituibles por sus clases base
-   **I**: Interface Segregation - Interfaces específicas mejor que interfaces generales
-   **D**: Dependency Inversion - Depender de abstracciones, no de concreciones

### Clean Architecture

-   Separación clara entre capas
-   Independencia de frameworks
-   Independencia de bases de datos
-   Testeable
-   Independiente de UI

### Clean Code

-   Nombres descriptivos
-   Funciones pequeñas
-   Comentarios solo cuando es necesario
-   Manejo de errores consistente
-   Tests como documentación

## 🤝 Contribución

1. Fork el proyecto
2. Crear feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la branch (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.
