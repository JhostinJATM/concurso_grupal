import os
import sys
import django
from django.conf import settings

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.contrib.auth.models import User
from apps.cajones_inteligentes.models import Cajon, Objeto

def crear_usuario_demo():
    """Crear un usuario demo si no existe"""
    try:
        user = User.objects.get(username='demo')
        print(f"✅ Usuario demo ya existe: {user.username}")
    except User.DoesNotExist:
        user = User.objects.create_user(
            username='demo',
            email='demo@test.com',
            password='demo123',
            first_name='Usuario',
            last_name='Demo'
        )
        print(f"✅ Usuario demo creado: {user.username}")
    return user

def crear_cajones(usuario):
    """Crear cajones de prueba"""
    cajones_data = [
        {
            'nombre': 'Cajón de Oficina',
            'capacidad_maxima': 15,
            'descripcion': 'Cajón para organizar materiales de oficina y papelería'
        },
        {
            'nombre': 'Cajón de Cocina',
            'capacidad_maxima': 20,
            'descripcion': 'Cajón para utensilios de cocina y artículos culinarios'
        },
        {
            'nombre': 'Cajón de Herramientas',
            'capacidad_maxima': 12,
            'descripcion': 'Cajón para almacenar herramientas de trabajo y bricolaje'
        },
        {
            'nombre': 'Cajón de Ropa',
            'capacidad_maxima': 25,
            'descripcion': 'Cajón para organizar prendas de vestir y accesorios'
        },
        {
            'nombre': 'Cajón de Electrónicos',
            'capacidad_maxima': 18,
            'descripcion': 'Cajón para cables, dispositivos y componentes electrónicos'
        },
        {
            'nombre': 'Cajón de Libros',
            'capacidad_maxima': 30,
            'descripcion': 'Cajón para almacenar libros y material de lectura'
        }
    ]
    
    cajones_creados = []
    print("\n🗃️ Creando cajones...")
    
    for cajon_info in cajones_data:
        cajon, created = Cajon.objects.get_or_create(
            nombre=cajon_info['nombre'],
            usuario=usuario,
            defaults={
                'capacidad_maxima': cajon_info['capacidad_maxima'],
                'descripcion': cajon_info['descripcion']
            }
        )
        if created:
            print(f"✅ Cajón creado: {cajon.nombre}")
        else:
            print(f"📋 Cajón ya existe: {cajon.nombre}")
        cajones_creados.append(cajon)
    
    return cajones_creados

def crear_objetos(cajones):
    """Crear objetos de prueba"""
    objetos_data = [
        # Objetos de oficina
        {'nombre': 'Grapadora roja', 'tipo_objeto': 'PAPELERIA', 'tamanio': 'PEQUENO', 'descripcion': 'Grapadora de oficina color rojo', 'cajon_tipo': 'Oficina'},
        {'nombre': 'Resma de papel A4', 'tipo_objeto': 'PAPELERIA', 'tamanio': 'GRANDE', 'descripcion': 'Paquete de 500 hojas blancas A4', 'cajon_tipo': 'Oficina'},
        {'nombre': 'Bolígrafos azules', 'tipo_objeto': 'PAPELERIA', 'tamanio': 'PEQUENO', 'descripcion': 'Caja de 10 bolígrafos azules', 'cajon_tipo': 'Oficina'},
        {'nombre': 'Calculadora científica', 'tipo_objeto': 'ELECTRONICA', 'tamanio': 'MEDIANO', 'descripcion': 'Calculadora con funciones avanzadas', 'cajon_tipo': 'Oficina'},
        {'nombre': 'Archivador verde', 'tipo_objeto': 'PAPELERIA', 'tamanio': 'GRANDE', 'descripcion': 'Archivador de palanca tamaño oficio', 'cajon_tipo': 'Oficina'},

        # Objetos de cocina
        {'nombre': 'Juego de cuchillos', 'tipo_objeto': 'COCINA', 'tamanio': 'GRANDE', 'descripcion': 'Set de 6 cuchillos de cocina', 'cajon_tipo': 'Cocina'},
        {'nombre': 'Tabla de cortar', 'tipo_objeto': 'COCINA', 'tamanio': 'MEDIANO', 'descripcion': 'Tabla de bambú para cortar alimentos', 'cajon_tipo': 'Cocina'},
        {'nombre': 'Batidor manual', 'tipo_objeto': 'COCINA', 'tamanio': 'MEDIANO', 'descripcion': 'Batidor de acero inoxidable', 'cajon_tipo': 'Cocina'},
        {'nombre': 'Moldes para hornear', 'tipo_objeto': 'COCINA', 'tamanio': 'GRANDE', 'descripcion': 'Set de 3 moldes antiadherentes', 'cajon_tipo': 'Cocina'},
        {'nombre': 'Especieros', 'tipo_objeto': 'COCINA', 'tamanio': 'PEQUENO', 'descripcion': 'Frascos para especias con etiquetas', 'cajon_tipo': 'Cocina'},

        # Herramientas
        {'nombre': 'Destornillador Phillips', 'tipo_objeto': 'HERRAMIENTAS', 'tamanio': 'PEQUENO', 'descripcion': 'Destornillador de punta Phillips mediano', 'cajon_tipo': 'Herramientas'},
        {'nombre': 'Martillo de carpintero', 'tipo_objeto': 'HERRAMIENTAS', 'tamanio': 'MEDIANO', 'descripcion': 'Martillo con mango de madera', 'cajon_tipo': 'Herramientas'},
        {'nombre': 'Nivel de burbuja', 'tipo_objeto': 'HERRAMIENTAS', 'tamanio': 'MEDIANO', 'descripcion': 'Nivel de 60cm con 3 burbujas', 'cajon_tipo': 'Herramientas'},
        {'nombre': 'Llave inglesa', 'tipo_objeto': 'HERRAMIENTAS', 'tamanio': 'MEDIANO', 'descripcion': 'Llave ajustable de 10 pulgadas', 'cajon_tipo': 'Herramientas'},
        {'nombre': 'Caja de tornillos', 'tipo_objeto': 'HERRAMIENTAS', 'tamanio': 'PEQUENO', 'descripcion': 'Surtido de tornillos diversos', 'cajon_tipo': 'Herramientas'},

        # Ropa
        {'nombre': 'Camisetas de algodón', 'tipo_objeto': 'ROPA', 'tamanio': 'MEDIANO', 'descripcion': 'Pack de 5 camisetas básicas', 'cajon_tipo': 'Ropa'},
        {'nombre': 'Jeans azules', 'tipo_objeto': 'ROPA', 'tamanio': 'MEDIANO', 'descripcion': 'Pantalón de mezclilla talla M', 'cajon_tipo': 'Ropa'},
        {'nombre': 'Calcetines deportivos', 'tipo_objeto': 'ROPA', 'tamanio': 'PEQUENO', 'descripcion': 'Paquete de 6 pares de calcetines', 'cajon_tipo': 'Ropa'},
        {'nombre': 'Chaqueta de invierno', 'tipo_objeto': 'ROPA', 'tamanio': 'GRANDE', 'descripcion': 'Chaqueta impermeable con capucha', 'cajon_tipo': 'Ropa'},
        {'nombre': 'Corbatas formales', 'tipo_objeto': 'ROPA', 'tamanio': 'PEQUENO', 'descripcion': 'Set de 3 corbatas de seda', 'cajon_tipo': 'Ropa'},

        # Electrónicos
        {'nombre': 'Cable USB-C', 'tipo_objeto': 'CABLES', 'tamanio': 'PEQUENO', 'descripcion': 'Cable de carga USB-C de 2 metros', 'cajon_tipo': 'Electrónicos'},
        {'nombre': 'Adaptador HDMI', 'tipo_objeto': 'ELECTRONICA', 'tamanio': 'PEQUENO', 'descripcion': 'Adaptador HDMI a VGA', 'cajon_tipo': 'Electrónicos'},
        {'nombre': 'Disco duro externo', 'tipo_objeto': 'ELECTRONICA', 'tamanio': 'PEQUENO', 'descripcion': 'HDD externo de 1TB', 'cajon_tipo': 'Electrónicos'},
        {'nombre': 'Router WiFi', 'tipo_objeto': 'ELECTRONICA', 'tamanio': 'MEDIANO', 'descripcion': 'Router dual band AC1200', 'cajon_tipo': 'Electrónicos'},
        {'nombre': 'Cables de red', 'tipo_objeto': 'CABLES', 'tamanio': 'MEDIANO', 'descripcion': 'Pack de 5 cables Ethernet Cat6', 'cajon_tipo': 'Electrónicos'},

        # Libros
        {'nombre': 'Novela de ciencia ficción', 'tipo_objeto': 'LIBROS', 'tamanio': 'MEDIANO', 'descripcion': 'Libro de 400 páginas de ciencia ficción', 'cajon_tipo': 'Libros'},
        {'nombre': 'Manual de programación', 'tipo_objeto': 'LIBROS', 'tamanio': 'GRANDE', 'descripcion': 'Guía completa de Python', 'cajon_tipo': 'Libros'},
        {'nombre': 'Revista de tecnología', 'tipo_objeto': 'LIBROS', 'tamanio': 'PEQUENO', 'descripcion': 'Revista mensual de tecnología', 'cajon_tipo': 'Libros'},
        {'nombre': 'Diccionario bilingüe', 'tipo_objeto': 'LIBROS', 'tamanio': 'GRANDE', 'descripcion': 'Diccionario Español-Inglés', 'cajon_tipo': 'Libros'},
        {'nombre': 'Comic de superhéroes', 'tipo_objeto': 'LIBROS', 'tamanio': 'PEQUENO', 'descripcion': 'Edición especial coleccionable', 'cajon_tipo': 'Libros'},

        # Objetos sin cajón específico
        {'nombre': 'Plantas artificiales', 'tipo_objeto': 'OTROS', 'tamanio': 'MEDIANO', 'descripcion': 'Decoración de plantas sintéticas', 'cajon_tipo': None},
        {'nombre': 'Marco de fotos', 'tipo_objeto': 'OTROS', 'tamanio': 'PEQUENO', 'descripcion': 'Marco de madera para foto 10x15', 'cajon_tipo': None},
        {'nombre': 'Velas aromáticas', 'tipo_objeto': 'OTROS', 'tamanio': 'PEQUENO', 'descripcion': 'Set de 3 velas de diferentes aromas', 'cajon_tipo': None},
        {'nombre': 'Organizador de escritorio', 'tipo_objeto': 'OTROS', 'tamanio': 'MEDIANO', 'descripcion': 'Organizador con compartimentos', 'cajon_tipo': 'Oficina'},
        {'nombre': 'Lámpara de mesa', 'tipo_objeto': 'ELECTRONICA', 'tamanio': 'MEDIANO', 'descripcion': 'Lámpara LED regulable', 'cajon_tipo': None}
    ]
    
    print("\n📦 Creando objetos...")
    
    for objeto_info in objetos_data:
        # Buscar el cajón apropiado
        cajon = None
        if objeto_info['cajon_tipo']:
            cajon = next((c for c in cajones if objeto_info['cajon_tipo'] in c.nombre), None)
        
        objeto_data = {
            'nombre': objeto_info['nombre'],
            'tipo_objeto': objeto_info['tipo_objeto'],
            'tamanio': objeto_info['tamanio'],
            'descripcion': objeto_info['descripcion'],
            'cajon': cajon
        }
        
        objeto, created = Objeto.objects.get_or_create(
            nombre=objeto_info['nombre'],
            defaults=objeto_data
        )
        
        if created:
            cajon_info = f" en {cajon.nombre}" if cajon else " sin asignar"
            print(f"✅ Objeto creado: {objeto.nombre}{cajon_info}")
        else:
            print(f"📋 Objeto ya existe: {objeto.nombre}")

def main():
    print("🚀 Iniciando creación de datos de prueba...\n")
    
    try:
        # Crear usuario demo
        usuario = crear_usuario_demo()
        
        # Crear cajones
        cajones = crear_cajones(usuario)
        
        # Crear objetos
        crear_objetos(cajones)
        
        print(f"\n🎉 ¡Datos de prueba creados exitosamente!")
        print(f"📈 Usuario: {usuario.username}")
        print(f"📈 Cajones: {Cajon.objects.filter(usuario=usuario).count()}")
        print(f"📈 Objetos: {Objeto.objects.count()}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
