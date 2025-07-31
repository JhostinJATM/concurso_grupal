"""
Prueba simplificada del servicio de recomendaciones.
Este script verifica que la lógica básica funciona correctamente.
"""

def simular_datos_usuario():
    """Simula datos de un usuario para probar la lógica."""
    return {
        'usuario': 'test_user',
        'total_cajones': 3,
        'total_objetos': 25,
        'cajones': [
            {
                'nombre': 'Cajón Electrónicos',
                'capacidad_maxima': 10,
                'objetos_actuales': 10,  # 100% lleno
                'capacidad_disponible': 0,
                'porcentaje_ocupacion': 100.0,
                'objetos': [
                    {'nombre': 'Cable USB', 'tipo': 'CABLES', 'tamanio': 'PEQUENO'},
                    {'nombre': 'Cargador móvil', 'tipo': 'ELECTRONICA', 'tamanio': 'MEDIANO'},
                    {'nombre': 'Auriculares', 'tipo': 'ELECTRONICA', 'tamanio': 'MEDIANO'},
                    {'nombre': 'Mouse', 'tipo': 'ELECTRONICA', 'tamanio': 'MEDIANO'},
                    # ... más objetos para llenar
                ],
                'tipos_objetos': {'CABLES': 4, 'ELECTRONICA': 6},
                'tamanios_objetos': {'PEQUENO': 4, 'MEDIANO': 6},
                'descripcion': 'Dispositivos electrónicos'
            },
            {
                'nombre': 'Cajón Papelería',
                'capacidad_maxima': 15,
                'objetos_actuales': 8,  # 53% lleno
                'capacidad_disponible': 7,
                'porcentaje_ocupacion': 53.3,
                'objetos': [
                    {'nombre': 'Bolígrafos', 'tipo': 'PAPELERIA', 'tamanio': 'PEQUENO'},
                    {'nombre': 'Cuaderno', 'tipo': 'PAPELERIA', 'tamanio': 'MEDIANO'},
                    {'nombre': 'Grapadora', 'tipo': 'PAPELERIA', 'tamanio': 'MEDIANO'},
                    # ... más objetos
                ],
                'tipos_objetos': {'PAPELERIA': 8},
                'tamanios_objetos': {'PEQUENO': 3, 'MEDIANO': 5},
                'descripcion': 'Materiales de oficina'
            },
            {
                'nombre': 'Cajón Herramientas',
                'capacidad_maxima': 12,
                'objetos_actuales': 2,  # 17% lleno (subutilizado)
                'capacidad_disponible': 10,
                'porcentaje_ocupacion': 16.7,
                'objetos': [
                    {'nombre': 'Destornillador', 'tipo': 'HERRAMIENTAS', 'tamanio': 'MEDIANO'},
                    {'nombre': 'Llaves Allen', 'tipo': 'HERRAMIENTAS', 'tamanio': 'PEQUENO'},
                ],
                'tipos_objetos': {'HERRAMIENTAS': 2},
                'tamanios_objetos': {'PEQUENO': 1, 'MEDIANO': 1},
                'descripcion': 'Herramientas pequeñas'
            }
        ]
    }


def generar_recomendaciones_fallback(datos_usuario):
    """Simula la generación de recomendaciones sin LLM."""
    recomendaciones = []
    
    # Analizar cajones sobrecargados
    for cajon in datos_usuario['cajones']:
        if cajon['porcentaje_ocupacion'] > 90:
            recomendaciones.append({
                'titulo': f"Cajón '{cajon['nombre']}' está sobrecargado",
                'descripcion': f"El cajón tiene {cajon['objetos_actuales']} objetos de {cajon['capacidad_maxima']} posibles ({cajon['porcentaje_ocupacion']:.1f}%). Considera redistribuir algunos objetos a otros cajones con más espacio disponible.",
                'tipo': 'ESPACIO',
                'prioridad': 'ALTA',
                'razon': 'Un cajón sobrecargado dificulta encontrar objetos y puede causar desorganización.'
            })
        elif cajon['porcentaje_ocupacion'] < 30:
            recomendaciones.append({
                'titulo': f"Cajón '{cajon['nombre']}' está subutilizado",
                'descripcion': f"Este cajón solo tiene {cajon['objetos_actuales']} objetos y puede almacenar {cajon['capacidad_maxima']} ({cajon['porcentaje_ocupacion']:.1f}% de uso). Podrías mover objetos de otros cajones aquí para optimizar el espacio.",
                'tipo': 'EFICIENCIA',
                'prioridad': 'MEDIA',
                'razon': 'Optimizar el uso del espacio disponible mejora la organización general.'
            })
    
    # Analizar tipos de objetos mezclados
    tipos_por_cajon = {}
    for cajon in datos_usuario['cajones']:
        if len(cajon['tipos_objetos']) > 3:
            tipos_por_cajon[cajon['nombre']] = cajon['tipos_objetos']
    
    if tipos_por_cajon:
        cajones_afectados = ', '.join(tipos_por_cajon.keys())
        recomendaciones.append({
            'titulo': 'Organizar objetos por categorías',
            'descripcion': f'Los cajones {cajones_afectados} tienen muchos tipos diferentes de objetos mezclados. Considera agrupar objetos similares en el mismo cajón para facilitar la búsqueda.',
            'tipo': 'ORGANIZACION',
            'prioridad': 'MEDIA',
            'razon': 'Agrupar objetos por tipo facilita encontrarlos y mantiene mejor orden.'
        })
    
    # Recomendación general de mantenimiento
    if datos_usuario['total_objetos'] > 20:
        recomendaciones.append({
            'titulo': 'Revisión periódica de objetos',
            'descripcion': f'Con {datos_usuario["total_objetos"]} objetos almacenados, es recomendable hacer una revisión mensual para eliminar objetos que ya no necesitas y reorganizar según tus necesidades actuales.',
            'tipo': 'MANTENIMIENTO',
            'prioridad': 'BAJA',
            'razon': 'El mantenimiento regular previene la acumulación innecesaria y mantiene la organización.'
        })
    
    return recomendaciones


def construir_prompt_llm(datos_usuario):
    """Simula la construcción del prompt para el LLM."""
    prompt = f"""
Analiza la organización actual de cajones del usuario '{datos_usuario['usuario']}' y genera recomendaciones específicas.

DATOS ACTUALES:
- Total de cajones: {datos_usuario['total_cajones']}
- Total de objetos: {datos_usuario['total_objetos']}

DETALLES POR CAJÓN:
"""
    
    for cajon in datos_usuario['cajones']:
        prompt += f"""
Cajón: {cajon['nombre']}
- Capacidad: {cajon['objetos_actuales']}/{cajon['capacidad_maxima']} objetos ({cajon['porcentaje_ocupacion']:.1f}% ocupado)
- Descripción: {cajon['descripcion']}
- Tipos de objetos: {', '.join([f"{tipo}: {count}" for tipo, count in cajon['tipos_objetos'].items()])}
- Tamaños: {', '.join([f"{tam}: {count}" for tam, count in cajon['tamanios_objetos'].items()])}
- Objetos: {', '.join([obj['nombre'] for obj in cajon['objetos']])}
"""
    
    prompt += """
INSTRUCCIONES:
Genera exactamente 3-5 recomendaciones específicas y prácticas en formato JSON con esta estructura:

{
  "recomendaciones": [
    {
      "titulo": "Título conciso de la recomendación",
      "descripcion": "Descripción detallada y específica de qué hacer",
      "tipo": "ORGANIZACION|ESPACIO|MANTENIMIENTO|SEGURIDAD|EFICIENCIA",
      "prioridad": "BAJA|MEDIA|ALTA|CRITICA",
      "razon": "Por qué es importante esta recomendación"
    }
  ]
}

CRITERIOS PARA LAS RECOMENDACIONES:
1. Optimización de espacio: Identifica cajones subutilizados o sobrecargados
2. Organización por categorías: Sugiere reagrupar objetos similares
3. Eficiencia de acceso: Mejora la facilidad de encontrar objetos
4. Mantenimiento: Sugiere limpieza o reorganización periódica
5. Aprovechamiento: Ideas para usar mejor el espacio disponible

Responde SOLO con el JSON válido, sin texto adicional.
"""
    
    return prompt


def probar_sistema_recomendaciones():
    """Prueba completa del sistema de recomendaciones."""
    
    print("=== PRUEBA DEL SISTEMA DE RECOMENDACIONES ===\n")
    
    # Simular datos de usuario
    datos_usuario = simular_datos_usuario()
    
    print(f"Usuario: {datos_usuario['usuario']}")
    print(f"Total de cajones: {datos_usuario['total_cajones']}")
    print(f"Total de objetos: {datos_usuario['total_objetos']}")
    
    print("\n=== ESTADO ACTUAL DE CAJONES ===")
    for cajon in datos_usuario['cajones']:
        print(f"\n📦 {cajon['nombre']}")
        print(f"   Ocupación: {cajon['objetos_actuales']}/{cajon['capacidad_maxima']} ({cajon['porcentaje_ocupacion']:.1f}%)")
        print(f"   Tipos: {cajon['tipos_objetos']}")
        print(f"   Objetos: {[obj['nombre'] for obj in cajon['objetos'][:3]]}...")
    
    print("\n=== GENERANDO RECOMENDACIONES (MODO FALLBACK) ===")
    
    # Generar recomendaciones
    recomendaciones = generar_recomendaciones_fallback(datos_usuario)
    
    print(f"\n✅ Se generaron {len(recomendaciones)} recomendaciones:")
    
    for i, rec in enumerate(recomendaciones, 1):
        print(f"\n{i}. 🎯 {rec['titulo']}")
        print(f"   📝 {rec['descripcion']}")
        print(f"   🏷️ Tipo: {rec['tipo']}")
        print(f"   ⚡ Prioridad: {rec['prioridad']}")
        print(f"   💡 Razón: {rec['razon']}")
    
    print(f"\n=== PROMPT PARA LLM ===")
    prompt = construir_prompt_llm(datos_usuario)
    print("Prompt generado (primeras 500 caracteres):")
    print(prompt[:500] + "...")
    
    print(f"\n=== RESULTADO SIMULADO ===")
    resultado = {
        'usuario': datos_usuario['usuario'],
        'total_cajones': datos_usuario['total_cajones'],
        'total_objetos': datos_usuario['total_objetos'],
        'recomendaciones': recomendaciones,
        'generado_con_ia': False,  # Modo fallback
        'total_recomendaciones_generadas': len(recomendaciones)
    }
    
    print("JSON de respuesta del endpoint:")
    import json
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
    
    print(f"\n✅ ¡Sistema de recomendaciones funcionando correctamente!")
    print(f"📋 Total de recomendaciones: {len(recomendaciones)}")
    print(f"🤖 Modo: {'IA (OpenAI)' if resultado['generado_con_ia'] else 'Fallback (Reglas)'}")


if __name__ == "__main__":
    try:
        probar_sistema_recomendaciones()
    except Exception as e:
        print(f"❌ Error durante la prueba: {str(e)}")
        import traceback
        traceback.print_exc()
