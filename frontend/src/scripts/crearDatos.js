// Script para crear datos de prueba usando los endpoints del backend
const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

// Datos de ejemplo para cajones
const cajonesDePrueba = [
  {
    nombre: 'Cajón de Oficina',
    capacidad_maxima: 15,
    descripcion: 'Cajón para organizar materiales de oficina y papelería'
  },
  {
    nombre: 'Cajón de Cocina',
    capacidad_maxima: 20,
    descripcion: 'Cajón para utensilios de cocina y artículos culinarios'
  },
  {
    nombre: 'Cajón de Herramientas',
    capacidad_maxima: 12,
    descripcion: 'Cajón para almacenar herramientas de trabajo y bricolaje'
  },
  {
    nombre: 'Cajón de Ropa',
    capacidad_maxima: 25,
    descripcion: 'Cajón para organizar prendas de vestir y accesorios'
  },
  {
    nombre: 'Cajón de Electrónicos',
    capacidad_maxima: 18,
    descripcion: 'Cajón para cables, dispositivos y componentes electrónicos'
  },
  {
    nombre: 'Cajón de Libros',
    capacidad_maxima: 30,
    descripcion: 'Cajón para almacenar libros y material de lectura'
  }
];

// Datos de ejemplo para objetos
const objetosDePrueba = [
  // Objetos de oficina
  { nombre: 'Grapadora roja', tipo_objeto: 'PAPELERIA', tamanio: 'PEQUENO', descripcion: 'Grapadora de oficina color rojo' },
  { nombre: 'Resma de papel A4', tipo_objeto: 'PAPELERIA', tamanio: 'GRANDE', descripcion: 'Paquete de 500 hojas blancas A4' },
  { nombre: 'Bolígrafos azules', tipo_objeto: 'PAPELERIA', tamanio: 'PEQUENO', descripcion: 'Caja de 10 bolígrafos azules' },
  { nombre: 'Calculadora científica', tipo_objeto: 'ELECTRONICA', tamanio: 'MEDIANO', descripcion: 'Calculadora con funciones avanzadas' },
  { nombre: 'Archivador verde', tipo_objeto: 'PAPELERIA', tamanio: 'GRANDE', descripcion: 'Archivador de palanca tamaño oficio' },

  // Objetos de cocina
  { nombre: 'Juego de cuchillos', tipo_objeto: 'COCINA', tamanio: 'GRANDE', descripcion: 'Set de 6 cuchillos de cocina' },
  { nombre: 'Tabla de cortar', tipo_objeto: 'COCINA', tamanio: 'MEDIANO', descripcion: 'Tabla de bambú para cortar alimentos' },
  { nombre: 'Batidor manual', tipo_objeto: 'COCINA', tamanio: 'MEDIANO', descripcion: 'Batidor de acero inoxidable' },
  { nombre: 'Moldes para hornear', tipo_objeto: 'COCINA', tamanio: 'GRANDE', descripcion: 'Set de 3 moldes antiadherentes' },
  { nombre: 'Especieros', tipo_objeto: 'COCINA', tamanio: 'PEQUENO', descripcion: 'Frascos para especias con etiquetas' },

  // Herramientas
  { nombre: 'Destornillador Phillips', tipo_objeto: 'HERRAMIENTAS', tamanio: 'PEQUENO', descripcion: 'Destornillador de punta Phillips mediano' },
  { nombre: 'Martillo de carpintero', tipo_objeto: 'HERRAMIENTAS', tamanio: 'MEDIANO', descripcion: 'Martillo con mango de madera' },
  { nombre: 'Nivel de burbuja', tipo_objeto: 'HERRAMIENTAS', tamanio: 'MEDIANO', descripcion: 'Nivel de 60cm con 3 burbujas' },
  { nombre: 'Llave inglesa', tipo_objeto: 'HERRAMIENTAS', tamanio: 'MEDIANO', descripcion: 'Llave ajustable de 10 pulgadas' },
  { nombre: 'Caja de tornillos', tipo_objeto: 'HERRAMIENTAS', tamanio: 'PEQUENO', descripcion: 'Surtido de tornillos diversos' },

  // Ropa
  { nombre: 'Camisetas de algodón', tipo_objeto: 'ROPA', tamanio: 'MEDIANO', descripcion: 'Pack de 5 camisetas básicas' },
  { nombre: 'Jeans azules', tipo_objeto: 'ROPA', tamanio: 'MEDIANO', descripcion: 'Pantalón de mezclilla talla M' },
  { nombre: 'Calcetines deportivos', tipo_objeto: 'ROPA', tamanio: 'PEQUENO', descripcion: 'Paquete de 6 pares de calcetines' },
  { nombre: 'Chaqueta de invierno', tipo_objeto: 'ROPA', tamanio: 'GRANDE', descripcion: 'Chaqueta impermeable con capucha' },
  { nombre: 'Corbatas formales', tipo_objeto: 'ROPA', tamanio: 'PEQUENO', descripcion: 'Set de 3 corbatas de seda' },

  // Electrónicos
  { nombre: 'Cable USB-C', tipo_objeto: 'CABLES', tamanio: 'PEQUENO', descripcion: 'Cable de carga USB-C de 2 metros' },
  { nombre: 'Adaptador HDMI', tipo_objeto: 'ELECTRONICA', tamanio: 'PEQUENO', descripcion: 'Adaptador HDMI a VGA' },
  { nombre: 'Disco duro externo', tipo_objeto: 'ELECTRONICA', tamanio: 'PEQUENO', descripcion: 'HDD externo de 1TB' },
  { nombre: 'Router WiFi', tipo_objeto: 'ELECTRONICA', tamanio: 'MEDIANO', descripcion: 'Router dual band AC1200' },
  { nombre: 'Cables de red', tipo_objeto: 'CABLES', tamanio: 'MEDIANO', descripcion: 'Pack de 5 cables Ethernet Cat6' },

  // Libros
  { nombre: 'Novela de ciencia ficción', tipo_objeto: 'LIBROS', tamanio: 'MEDIANO', descripcion: 'Libro de 400 páginas de ciencia ficción' },
  { nombre: 'Manual de programación', tipo_objeto: 'LIBROS', tamanio: 'GRANDE', descripcion: 'Guía completa de Python' },
  { nombre: 'Revista de tecnología', tipo_objeto: 'LIBROS', tamanio: 'PEQUENO', descripcion: 'Revista mensual de tecnología' },
  { nombre: 'Diccionario bilingüe', tipo_objeto: 'LIBROS', tamanio: 'GRANDE', descripcion: 'Diccionario Español-Inglés' },
  { nombre: 'Comic de superhéroes', tipo_objeto: 'LIBROS', tamanio: 'PEQUENO', descripcion: 'Edición especial coleccionable' },

  // Otros objetos diversos
  { nombre: 'Plantas artificiales', tipo_objeto: 'OTROS', tamanio: 'MEDIANO', descripcion: 'Decoración de plantas sintéticas' },
  { nombre: 'Marco de fotos', tipo_objeto: 'OTROS', tamanio: 'PEQUENO', descripcion: 'Marco de madera para foto 10x15' },
  { nombre: 'Velas aromáticas', tipo_objeto: 'OTROS', tamanio: 'PEQUENO', descripcion: 'Set de 3 velas de diferentes aromas' },
  { nombre: 'Organizador de escritorio', tipo_objeto: 'OTROS', tamanio: 'MEDIANO', descripcion: 'Organizador con compartimentos' },
  { nombre: 'Lámpara de mesa', tipo_objeto: 'ELECTRONICA', tamanio: 'MEDIANO', descripcion: 'Lámpara LED regulable' }
];

// Función para crear cajones
async function crearCajones() {
  console.log('🗃️ Creando cajones...');
  const cajones = [];
  
  for (const cajon of cajonesDePrueba) {
    try {
      const response = await fetch(`${API_BASE_URL}/cajones/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(cajon)
      });
      
      if (response.ok) {
        const nuevoCajon = await response.json();
        cajones.push(nuevoCajon);
        console.log(`✅ Cajón creado: ${nuevoCajon.nombre} (ID: ${nuevoCajon.id})`);
      } else {
        const error = await response.text();
        console.error(`❌ Error creando cajón ${cajon.nombre}:`, error);
      }
    } catch (error) {
      console.error(`❌ Error de red creando cajón ${cajon.nombre}:`, error);
    }
  }
  
  return cajones;
}

// Función para crear objetos
async function crearObjetos(cajones) {
  console.log('📦 Creando objetos...');
  
  for (let i = 0; i < objetosDePrueba.length; i++) {
    const objeto = { ...objetosDePrueba[i] };
    
    // Asignar objetos a cajones de forma inteligente
    let cajonAsignado = null;
    
    // Intentar asignar a un cajón relacionado por tipo
    if (objeto.tipo_objeto === 'PAPELERIA' || objeto.tipo_objeto === 'ELECTRONICA') {
      cajonAsignado = cajones.find(c => c.nombre.includes('Oficina'));
    } else if (objeto.tipo_objeto === 'COCINA') {
      cajonAsignado = cajones.find(c => c.nombre.includes('Cocina'));
    } else if (objeto.tipo_objeto === 'HERRAMIENTAS') {
      cajonAsignado = cajones.find(c => c.nombre.includes('Herramientas'));
    } else if (objeto.tipo_objeto === 'ROPA') {
      cajonAsignado = cajones.find(c => c.nombre.includes('Ropa'));
    } else if (objeto.tipo_objeto === 'CABLES') {
      cajonAsignado = cajones.find(c => c.nombre.includes('Electrónicos'));
    } else if (objeto.tipo_objeto === 'LIBROS') {
      cajonAsignado = cajones.find(c => c.nombre.includes('Libros'));
    }
    
    // Si no se encuentra un cajón específico, asignar a uno aleatorio
    if (!cajonAsignado && cajones.length > 0) {
      cajonAsignado = cajones[Math.floor(Math.random() * cajones.length)];
    }
    
    // Algunos objetos los dejamos sin asignar (sin cajón)
    if (i % 7 !== 0 && cajonAsignado) {
      objeto.cajon = cajonAsignado.id;
    }
    
    try {
      const response = await fetch(`${API_BASE_URL}/objetos/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(objeto)
      });
      
      if (response.ok) {
        const nuevoObjeto = await response.json();
        const cajonInfo = cajonAsignado ? `en cajón ${cajonAsignado.nombre}` : 'sin asignar';
        console.log(`✅ Objeto creado: ${nuevoObjeto.nombre} (${cajonInfo})`);
      } else {
        const error = await response.text();
        console.error(`❌ Error creando objeto ${objeto.nombre}:`, error);
      }
    } catch (error) {
      console.error(`❌ Error de red creando objeto ${objeto.nombre}:`, error);
    }
  }
}

// Función principal
async function crearDatosDePrueba() {
  console.log('🚀 Iniciando creación de datos de prueba...\n');
  
  try {
    // Crear cajones primero
    const cajones = await crearCajones();
    console.log(`\n📊 Se crearon ${cajones.length} cajones exitosamente\n`);
    
    // Luego crear objetos
    await crearObjetos(cajones);
    console.log(`\n🎉 ¡Datos de prueba creados exitosamente!`);
    console.log(`📈 Total: ${cajones.length} cajones y ${objetosDePrueba.length} objetos`);
    
  } catch (error) {
    console.error('❌ Error general:', error);
  }
}

// Ejecutar el script
crearDatosDePrueba();
