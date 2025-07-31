# API de Recomendaciones Inteligentes

## Endpoint: Generar Recomendaciones Automáticas

### POST `/api/cajones_inteligentes/recomendaciones/generar_automaticas/`

Este endpoint utiliza inteligencia artificial (LLM) para analizar los cajones y objetos de un usuario y generar recomendaciones automáticas para optimizar la organización.

### Autenticación

Requiere autenticación. El token de autenticación debe incluirse en el header:

```
Authorization: Bearer <token>
```

### Parámetros de Entrada

**Body (JSON):**

```json
{
    "usuario_id": 123 // Opcional: ID del usuario. Si no se proporciona, usa el usuario autenticado
}
```

**Nota:** Solo los administradores pueden generar recomendaciones para otros usuarios. Los usuarios normales solo pueden generar recomendaciones para sí mismos.

### Respuesta Exitosa (201 Created)

```json
{
    "usuario": "nombre_usuario",
    "total_cajones": 5,
    "total_objetos": 47,
    "recomendaciones": [
        {
            "titulo": "Optimizar cajón de electrónicos",
            "descripcion": "El cajón 'Electrónicos' está al 95% de capacidad. Considera redistribuir algunos cables a otro cajón.",
            "tipo": "ESPACIO",
            "prioridad": "ALTA",
            "razon": "Un cajón sobrecargado dificulta encontrar objetos rápidamente"
        },
        {
            "titulo": "Agrupar objetos de papelería",
            "descripcion": "Tienes objetos de papelería dispersos en 3 cajones diferentes. Centralízalos en uno solo.",
            "tipo": "ORGANIZACION",
            "prioridad": "MEDIA",
            "razon": "Agrupar objetos similares mejora la eficiencia de búsqueda"
        }
    ],
    "generado_con_ia": true,
    "recomendaciones_guardadas": [
        {
            "id": 45,
            "nombre": "Optimizar cajón de electrónicos",
            "descripcion": "El cajón 'Electrónicos' está al 95% de capacidad...",
            "prioridad": "ALTA",
            "tipo_recomendacion": "ESPACIO",
            "implementada": false,
            "fecha_creacion": "2025-07-31",
            "fecha_implementacion": null,
            "created_at": "2025-07-31T10:30:00Z",
            "updated_at": "2025-07-31T10:30:00Z"
        }
    ],
    "total_recomendaciones_generadas": 5
}
```

### Respuestas de Error

**400 Bad Request - Usuario no encontrado:**

```json
{
    "error": "Usuario no encontrado"
}
```

**403 Forbidden - Sin permisos:**

```json
{
    "error": "No tienes permisos para generar recomendaciones para otro usuario"
}
```

**500 Internal Server Error:**

```json
{
    "error": "Error interno del servidor: <detalle del error>"
}
```

### Tipos de Recomendaciones

El sistema puede generar los siguientes tipos de recomendaciones:

1. **ORGANIZACION**: Sugerencias para mejorar la organización de objetos
2. **ESPACIO**: Optimización del uso del espacio disponible
3. **MANTENIMIENTO**: Tareas de limpieza y mantenimiento periódico
4. **SEGURIDAD**: Recomendaciones de seguridad para objetos importantes
5. **EFICIENCIA**: Mejoras para acceder más rápido a los objetos

### Niveles de Prioridad

-   **BAJA**: Recomendaciones opcionales de mejora
-   **MEDIA**: Sugerencias importantes para mejor organización
-   **ALTA**: Problemas que requieren atención pronta
-   **CRITICA**: Problemas urgentes que afectan la funcionalidad

### Configuración

Para habilitar las recomendaciones con IA, configura las siguientes variables de entorno:

```bash
# Requerido para usar OpenAI
OPENAI_API_KEY=tu_api_key_de_openai

# Opcional - configuraciones avanzadas
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_MAX_TOKENS=1500
RECOMENDACIONES_IA_ENABLED=true
RECOMENDACIONES_MAX_POR_USUARIO=10
```

### Modo Fallback

Si no se configura `OPENAI_API_KEY`, el sistema funcionará en modo fallback generando recomendaciones básicas basadas en reglas predefinidas:

-   Detecta cajones sobrecargados (>90% capacidad)
-   Identifica cajones subutilizados (<30% capacidad)
-   Sugiere organización por categorías cuando hay muchos tipos mezclados
-   Recomienda mantenimiento periódico para usuarios con muchos objetos

### Ejemplo de Uso con cURL

```bash
curl -X POST \
  http://localhost:8000/api/cajones_inteligentes/recomendaciones/generar_automaticas/ \
  -H 'Authorization: Bearer tu_token_aqui' \
  -H 'Content-Type: application/json' \
  -d '{
    "usuario_id": 123
  }'
```

### Ejemplo de Uso con JavaScript

```javascript
const response = await fetch(
    "/api/cajones_inteligentes/recomendaciones/generar_automaticas/",
    {
        method: "POST",
        headers: {
            Authorization: "Bearer " + token,
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            usuario_id: 123, // Opcional
        }),
    }
);

const data = await response.json();
console.log("Recomendaciones generadas:", data);
```

### Notas de Implementación

1. Las recomendaciones se guardan automáticamente en la base de datos
2. El endpoint analiza todos los cajones activos del usuario
3. Se generan máximo 5 recomendaciones por llamada
4. Las recomendaciones incluyen contexto específico del estado actual
5. El sistema evita generar recomendaciones duplicadas recientes
