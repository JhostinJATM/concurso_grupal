# Sistema de Recomendaciones Inteligentes

## Funcionalidad Implementada

Se ha implementado un sistema de recomendaciones automáticas que utiliza un LLM (Large Language Model) para analizar el contenido de los cajones de un usuario y generar sugerencias inteligentes de organización.

## Archivos Creados/Modificados

### 1. Servicio de Recomendaciones

-   **`apps/cajones_inteligentes/services.py`**: Servicio principal que maneja la lógica de recomendaciones con LLM

### 2. Endpoint API

-   **`apps/cajones_inteligentes/views.py`**: Agregado endpoint `generar_automaticas` en `RecomendacionViewSet`

### 3. Configuración

-   **`config/settings/base.py`**: Agregada configuración para OpenAI y recomendaciones IA
-   **`requirements/base.txt`**: Agregada dependencia `openai==1.54.4`
-   **`.env.example`**: Agregadas variables de entorno necesarias

### 4. Documentación

-   **`docs/API_RECOMENDACIONES.md`**: Documentación completa del endpoint

## Endpoint Implementado

### POST `/api/cajones_inteligentes/recomendaciones/generar_automaticas/`

Este endpoint:

1. Recibe el ID de un usuario (opcional, por defecto usa el usuario autenticado)
2. Analiza todos los cajones y objetos del usuario
3. Envía los datos al LLM con un prompt especializado
4. Genera recomendaciones inteligentes
5. Guarda las recomendaciones en la base de datos
6. Retorna un JSON con las recomendaciones generadas

## Características del Sistema

### Análisis Inteligente

-   **Detección de sobrecarga**: Identifica cajones con más del 90% de capacidad
-   **Detección de subutilización**: Encuentra cajones con menos del 30% de uso
-   **Análisis de categorías**: Identifica objetos mezclados que podrían organizarse mejor
-   **Contexto temporal**: Considera cuándo se agregaron los objetos

### Tipos de Recomendaciones

1. **ORGANIZACION**: Mejoras en la agrupación de objetos
2. **ESPACIO**: Optimización del uso del espacio disponible
3. **MANTENIMIENTO**: Tareas de limpieza y mantenimiento
4. **SEGURIDAD**: Protección de objetos importantes
5. **EFICIENCIA**: Mejoras para acceso más rápido

### Niveles de Prioridad

-   **BAJA**: Mejoras opcionales
-   **MEDIA**: Recomendaciones importantes
-   **ALTA**: Problemas que requieren atención
-   **CRITICA**: Problemas urgentes

## Configuración Requerida

### Variables de Entorno

```bash
# Requerido para usar OpenAI
OPENAI_API_KEY=sk-tu_api_key_aqui

# Opcional - configuraciones avanzadas
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_MAX_TOKENS=1500
RECOMENDACIONES_IA_ENABLED=true
RECOMENDACIONES_MAX_POR_USUARIO=10
```

### Instalación de Dependencias

```bash
pip install openai==1.54.4
```

## Ejemplo de Uso

### Request

```bash
curl -X POST \\
  http://localhost:8000/api/cajones_inteligentes/recomendaciones/generar_automaticas/ \\
  -H 'Authorization: Bearer tu_token' \\
  -H 'Content-Type: application/json' \\
  -d '{"usuario_id": 123}'
```

### Response

```json
{
    "usuario": "juan_perez",
    "total_cajones": 3,
    "total_objetos": 25,
    "recomendaciones": [
        {
            "titulo": "Redistribuir cables del cajón de electrónicos",
            "descripcion": "El cajón 'Electrónicos' está al 100% de capacidad...",
            "tipo": "ESPACIO",
            "prioridad": "ALTA",
            "razon": "Un cajón sobrecargado dificulta encontrar objetos"
        }
    ],
    "generado_con_ia": true,
    "total_recomendaciones_generadas": 3
}
```

## Modo Fallback

Si no se configura `OPENAI_API_KEY`, el sistema funciona en modo fallback con reglas predefinidas:

-   Detección de cajones sobrecargados (>90%)
-   Detección de cajones subutilizados (<30%)
-   Sugerencias de organización por categorías
-   Recomendaciones de mantenimiento periódico

## Integración con Frontend

El endpoint está listo para ser consumido desde el frontend React. El componente puede:

1. Llamar al endpoint después de que el usuario termine de organizar
2. Mostrar las recomendaciones en una interfaz amigable
3. Permitir marcar recomendaciones como implementadas
4. Mostrar el historial de recomendaciones

## Ejemplo de Integración React

```javascript
const generarRecomendaciones = async () => {
    try {
        const response = await fetch(
            "/api/cajones_inteligentes/recomendaciones/generar_automaticas/",
            {
                method: "POST",
                headers: {
                    Authorization: `Bearer ${token}`,
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    usuario_id: userId, // Opcional
                }),
            }
        );

        const data = await response.json();

        if (response.ok) {
            setRecomendaciones(data.recomendaciones);
            setGeneradoConIA(data.generado_con_ia);
        } else {
            console.error("Error:", data.error);
        }
    } catch (error) {
        console.error("Error de red:", error);
    }
};
```

## Próximos Pasos

1. **Testing**: Ejecutar pruebas con datos reales
2. **Configuración**: Agregar tu API key de OpenAI
3. **Frontend**: Integrar con la interfaz de usuario
4. **Optimización**: Ajustar prompts según feedback de usuarios
5. **Monitoreo**: Agregar logs para análisis de uso

## Beneficios

-   **Automatización**: Las recomendaciones se generan automáticamente
-   **Personalización**: Cada recomendación es específica para el usuario
-   **Inteligencia**: Usa IA avanzada para análisis contextual
-   **Escalabilidad**: Funciona con cualquier cantidad de cajones/objetos
-   **Flexibilidad**: Modo fallback cuando no hay IA disponible

El sistema está completamente funcional y listo para ser probado con datos reales.
