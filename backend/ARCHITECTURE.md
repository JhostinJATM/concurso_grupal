# Estructura del Proyecto Smart Drawers Backend

## 📁 Árbol de Directorios

```
backend/
├── 📁 .git/                          # Control de versiones Git
├── 📁 .venv/                         # Entorno virtual Python
├── 📁 apps/                          # 🏗️ Aplicaciones del dominio
│   └── 📄 __init__.py               # Inicializador del paquete apps
├── 📁 config/                        # ⚙️ Configuración del proyecto
│   ├── 📁 settings/                 # Configuraciones por ambiente
│   │   ├── 📄 __init__.py          # Selector de configuración por ambiente
│   │   ├── 📄 base.py              # ⚙️ Configuración base común
│   │   ├── 📄 development.py       # 🛠️ Configuración de desarrollo
│   │   ├── 📄 production.py        # 🚀 Configuración de producción
│   │   └── 📄 testing.py           # 🧪 Configuración para testing
│   ├── 📄 urls.py                   # 🌐 URLs principales del proyecto
│   ├── 📄 wsgi.py                   # 🔌 WSGI application
│   └── 📄 asgi.py                   # 🔌 ASGI application
├── 📁 core/                          # 🎯 Módulo core (funcionalidades base)
│   ├── 📄 __init__.py              # Inicializador del core
│   ├── 📄 models.py                # 📊 Modelos base abstractos
│   ├── 📄 views.py                 # 👁️ Views base y HealthCheck
│   ├── 📄 serializers.py           # 🔄 Serializadores base
│   └── 📄 urls.py                  # 🌐 URLs del core (health check)
├── 📁 utils/                         # 🛠️ Utilidades comunes
│   ├── 📄 __init__.py              # Inicializador de utilidades
│   ├── 📄 exceptions.py            # ⚠️ Excepciones personalizadas
│   ├── 📄 validators.py            # ✅ Validadores personalizados
│   └── 📄 helpers.py               # 🤝 Funciones de ayuda
├── 📁 requirements/                  # 📦 Gestión de dependencias
│   ├── 📄 base.txt                 # Dependencias básicas
│   ├── 📄 development.txt          # Dependencias de desarrollo
│   ├── 📄 production.txt           # Dependencias de producción
│   └── 📄 testing.txt              # Dependencias para testing
├── 📁 static/                        # 🎨 Archivos estáticos
├── 📁 media/                         # 📷 Archivos multimedia
├── 📁 templates/                     # 📋 Templates HTML
├── 📁 tests/                         # 🧪 Tests del proyecto
│   ├── 📄 test_base.py             # Tests base
│   └── 📄 test_core.py             # Tests del core
├── 📁 logs/                          # 📝 Archivos de log
│   └── 📄 .gitkeep                 # Mantener directorio en git
├── 📄 .env.example                  # 🔧 Ejemplo de configuración de entorno
├── 📄 .gitignore                    # 🚫 Archivos ignorados por Git
├── 📄 .flake8                       # 📏 Configuración de Flake8
├── 📄 manage.py                     # 🎮 Utilidad de línea de comandos Django
├── 📄 pytest.ini                    # 🧪 Configuración de Pytest
├── 📄 pyproject.toml                # 📦 Configuración de herramientas Python
├── 📄 README.md                     # 📖 Documentación principal
├── 📄 setup.sh                      # 🐧 Script de configuración (Linux/Mac)
├── 📄 setup.bat                     # 🪟 Script de configuración (Windows)
└── 📄 ARCHITECTURE.md               # 🏗️ Este archivo
```

## 🏗️ Principios Arquitectónicos Aplicados

### 1. **Clean Architecture** 🧽

-   **Separación de capas**: Core, Apps, Utils
-   **Independencia de frameworks**: Lógica de negocio separada de Django
-   **Inversión de dependencias**: Abstracciones en el core
-   **Testeable**: Estructura que facilita el testing

### 2. **Principios SOLID** 🎯

#### **S** - Single Responsibility Principle

-   Cada módulo tiene una responsabilidad específica
-   `core/models.py`: Solo modelos base
-   `core/views.py`: Solo views base
-   `utils/validators.py`: Solo validaciones

#### **O** - Open/Closed Principle

-   Clases base abiertas para extensión, cerradas para modificación
-   `BaseModel` puede ser extendido sin modificar su código
-   `BaseViewSet` permite extensión mediante herencia

#### **L** - Liskov Substitution Principle

-   Las subclases son sustituibles por sus clases base
-   Cualquier modelo que herede de `BaseModel` mantiene el contrato
-   Views que hereden de `BaseViewSet` funcionan como esperado

#### **I** - Interface Segregation Principle

-   Interfaces específicas y pequeñas
-   Serializadores especializados por funcionalidad
-   Validadores específicos por tipo de dato

#### **D** - Dependency Inversion Principle

-   Dependencia de abstracciones, no de concreciones
-   Uso de settings modulares
-   Inyección de dependencias en views

### 3. **Domain-Driven Design (DDD)** 🎯

-   **Apps como bounded contexts**: Cada app representa un dominio
-   **Core como shared kernel**: Funcionalidades compartidas
-   **Value objects**: Modelos con validaciones específicas del dominio

### 4. **Clean Code** ✨

-   **Nombres descriptivos**: Variables y funciones con nombres claros
-   **Funciones pequeñas**: Una responsabilidad por función
-   **Comentarios útiles**: Documentación que agrega valor
-   **Estructura consistente**: Patrones aplicados uniformemente

## 📂 Patrones de Diseño Utilizados

### 1. **Repository Pattern**

-   Implementado a través de Django ORM y QuerySets
-   `BaseViewSet` actúa como repositorio base

### 2. **Strategy Pattern**

-   Validadores implementan diferentes estrategias
-   Settings modulares por ambiente

### 3. **Template Method Pattern**

-   `BaseModel` define el template para modelos
-   `BaseViewSet` define el template para views

### 4. **Singleton Pattern**

-   `SingletonMeta` en `utils/helpers.py`
-   Para configuraciones que deben ser únicas

## 🔄 Flujo de Datos

```
Request → URLs → Views → Serializers → Models → Database
Response ← Views ← Serializers ← Models ← Database
```

### 1. **Entrada de Request**

-   `config/urls.py` → Routing principal
-   `app/urls.py` → Routing específico de app
-   `views.py` → Procesamiento de lógica

### 2. **Procesamiento**

-   `serializers.py` → Validación y transformación
-   `models.py` → Interacción con base de datos
-   `utils/` → Funciones de apoyo

### 3. **Respuesta**

-   `serializers.py` → Formateo de salida
-   `views.py` → Preparación de response
-   Cliente ← Response JSON

## 🚀 Escalabilidad y Mantenibilidad

### Estructura Modular

-   **Apps independientes**: Cada funcionalidad en su propio módulo
-   **Core reutilizable**: Funcionalidades base compartidas
-   **Utils centralizadas**: Evita duplicación de código

### Configuración Flexible

-   **Settings por ambiente**: Development, Production, Testing
-   **Variables de entorno**: Configuración externa
-   **Logging estructurado**: Monitoreo y debugging

### Testing Estratificado

-   **Tests unitarios**: Por modelo, view, serializer
-   **Tests de integración**: Flujos completos
-   **Tests de API**: Endpoints completos

## 📈 Próximos Pasos para Desarrollo

### 1. **Crear Apps de Dominio**

```bash
cd apps
python ../manage.py startapp drawers
python ../manage.py startapp sensors
python ../manage.py startapp intelligence
```

### 2. **Implementar Modelos de Dominio**

-   Heredar de `BaseModel` o `AuditableModel`
-   Usar validadores personalizados
-   Implementar lógica de negocio en métodos del modelo

### 3. **Crear APIs REST**

-   Heredar de `BaseViewSet` o `ReadOnlyBaseViewSet`
-   Implementar serializadores específicos
-   Configurar permisos y autenticación

### 4. **Agregar Testing**

-   Tests unitarios por funcionalidad
-   Tests de integración para flujos completos
-   Coverage mínimo del 80%

Esta arquitectura proporciona una base sólida, escalable y mantenible para el desarrollo del sistema Smart Drawers Backend. 🎯
