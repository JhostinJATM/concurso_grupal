"""
Pruebas para el servicio de recomendaciones.
"""

import os
import sys
import django

# Configurar Django
sys.path.append('c:/Users/Axlmd/Desktop/concurso_grupal/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.contrib.auth.models import User
from apps.cajones_inteligentes.models import Cajon, Objeto, TipoObjeto, Tamanio
from apps.cajones_inteligentes.services import RecomendacionService


def crear_datos_prueba():
    """Crear datos de prueba para testing."""
    
    # Crear usuario de prueba
    usuario, created = User.objects.get_or_create(
        username='test_recomendaciones',
        defaults={
            'email': 'test@example.com',
            'first_name': 'Usuario',
            'last_name': 'Prueba'
        }
    )
    
    if created:
        print(f"✓ Usuario creado: {usuario.username}")
    else:
        print(f"✓ Usuario existente: {usuario.username}")
    
    # Crear cajones de prueba
    cajones_data = [
        {'nombre': 'Cajón Electrónicos', 'capacidad_maxima': 10, 'descripcion': 'Para dispositivos electrónicos'},
        {'nombre': 'Cajón Papelería', 'capacidad_maxima': 15, 'descripcion': 'Materiales de oficina'},
        {'nombre': 'Cajón Herramientas', 'capacidad_maxima': 8, 'descripcion': 'Herramientas pequeñas'},
    ]
    
    cajones = []
    for data in cajones_data:
        cajon, created = Cajon.objects.get_or_create(
            nombre=data['nombre'],
            usuario=usuario,
            defaults=data
        )
        cajones.append(cajon)
        if created:
            print(f"✓ Cajón creado: {cajon.nombre}")
        else:
            print(f"✓ Cajón existente: {cajon.nombre}")
    
    # Crear objetos de prueba
    objetos_data = [
        # Muchos objetos en el cajón de electrónicos (sobrecargado)
        {'nombre': 'Cable USB', 'tipo_objeto': TipoObjeto.CABLES, 'cajon': cajones[0]},
        {'nombre': 'Cargador móvil', 'tipo_objeto': TipoObjeto.ELECTRONICA, 'cajon': cajones[0]},
        {'nombre': 'Auriculares', 'tipo_objeto': TipoObjeto.ELECTRONICA, 'cajon': cajones[0]},
        {'nombre': 'Adaptador HDMI', 'tipo_objeto': TipoObjeto.CABLES, 'cajon': cajones[0]},
        {'nombre': 'Mouse inalámbrico', 'tipo_objeto': TipoObjeto.ELECTRONICA, 'cajon': cajones[0]},
        {'nombre': 'Cable ethernet', 'tipo_objeto': TipoObjeto.CABLES, 'cajon': cajones[0]},
        {'nombre': 'Pendrive 32GB', 'tipo_objeto': TipoObjeto.ELECTRONICA, 'cajon': cajones[0]},
        {'nombre': 'Cargador laptop', 'tipo_objeto': TipoObjeto.ELECTRONICA, 'cajon': cajones[0]},
        {'nombre': 'Cable audio', 'tipo_objeto': TipoObjeto.CABLES, 'cajon': cajones[0]},
        {'nombre': 'Hub USB', 'tipo_objeto': TipoObjeto.ELECTRONICA, 'cajon': cajones[0]},
        
        # Algunos objetos en papelería
        {'nombre': 'Bolígrafos', 'tipo_objeto': TipoObjeto.PAPELERIA, 'cajon': cajones[1]},
        {'nombre': 'Cuaderno', 'tipo_objeto': TipoObjeto.PAPELERIA, 'cajon': cajones[1]},
        {'nombre': 'Grapadora', 'tipo_objeto': TipoObjeto.PAPELERIA, 'cajon': cajones[1]},
        
        # Pocos objetos en herramientas (subutilizado)
        {'nombre': 'Destornillador', 'tipo_objeto': TipoObjeto.HERRAMIENTAS, 'cajon': cajones[2]},
    ]
    
    for data in objetos_data:
        objeto, created = Objeto.objects.get_or_create(
            nombre=data['nombre'],
            cajon=data['cajon'],
            defaults={
                'tipo_objeto': data['tipo_objeto'],
                'tamanio': Tamanio.MEDIANO
            }
        )
        if created:
            print(f"✓ Objeto creado: {objeto.nombre} -> {objeto.cajon.nombre}")
    
    return usuario


def probar_recomendaciones():
    """Probar el servicio de recomendaciones."""
    
    print("=== PRUEBA DEL SERVICIO DE RECOMENDACIONES ===\n")
    
    # Crear datos de prueba
    usuario = crear_datos_prueba()
    
    print(f"\n=== DATOS DEL USUARIO: {usuario.username} ===")
    
    # Mostrar estado actual
    cajones = Cajon.objects.filter(usuario=usuario, is_active=True)
    print(f"Total de cajones: {cajones.count()}")
    
    for cajon in cajones:
        objetos_count = cajon.objetos.filter(is_active=True).count()
        print(f"- {cajon.nombre}: {objetos_count}/{cajon.capacidad_maxima} objetos ({cajon.porcentaje_uso:.1f}%)")
        
        objetos = cajon.objetos.filter(is_active=True)
        for obj in objetos:
            print(f"  * {obj.nombre} ({obj.tipo_objeto})")
    
    print(f"\n=== GENERANDO RECOMENDACIONES ===")
    
    # Probar el servicio
    servicio = RecomendacionService()
    resultado = servicio.generar_recomendaciones_usuario(usuario.id)
    
    print(f"Resultado: {resultado}")
    
    if 'error' in resultado:
        print(f"❌ Error: {resultado['error']}")
        return
    
    print(f"✓ Generado con IA: {resultado.get('generado_con_ia', False)}")
    print(f"✓ Total de recomendaciones: {len(resultado.get('recomendaciones', []))}")
    
    print(f"\n=== RECOMENDACIONES GENERADAS ===")
    for i, rec in enumerate(resultado.get('recomendaciones', []), 1):
        print(f"\n{i}. {rec.get('titulo', 'Sin título')}")
        print(f"   Tipo: {rec.get('tipo', 'N/A')}")
        print(f"   Prioridad: {rec.get('prioridad', 'N/A')}")
        print(f"   Descripción: {rec.get('descripcion', 'N/A')}")
        print(f"   Razón: {rec.get('razon', 'N/A')}")


if __name__ == "__main__":
    try:
        probar_recomendaciones()
    except Exception as e:
        print(f"❌ Error durante la prueba: {str(e)}")
        import traceback
        traceback.print_exc()
