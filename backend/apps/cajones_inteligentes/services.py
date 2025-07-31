"""
Servicios para la aplicación de Cajones Inteligentes.
Implementa la lógica de negocio para recomendaciones con LLM.
"""

import json
import logging
from typing import Dict, List, Any
from django.conf import settings
from django.contrib.auth.models import User
from decouple import config
import openai

from .models import Cajon, Objeto, Recomendacion, TipoObjeto, Tamanio

logger = logging.getLogger(__name__)


class RecomendacionService:
    """
    Servicio para generar recomendaciones inteligentes usando LLM.
    Analiza los cajones y objetos del usuario para generar sugerencias de organización.
    """
    
    def __init__(self):
        """Inicializa el servicio con la configuración de OpenAI."""
        api_key = config('OPENAI_API_KEY', default='')
        if not api_key:
            logger.warning("OPENAI_API_KEY no configurada. Las recomendaciones estarán limitadas.")
            self.client = None
        else:
            self.client = openai.OpenAI(api_key=api_key)
    
    def generar_recomendaciones_usuario(self, usuario_id: int) -> Dict[str, Any]:
        """
        Genera recomendaciones para un usuario específico basado en sus cajones y objetos.
        
        Args:
            usuario_id: ID del usuario
            
        Returns:
            Dict con las recomendaciones generadas
        """
        try:
            # Obtener el usuario
            usuario = User.objects.get(id=usuario_id)
            
            # Obtener datos del usuario
            datos_usuario = self._recopilar_datos_usuario(usuario)
            
            # Generar recomendaciones con LLM
            if self.client:
                recomendaciones_llm = self._generar_con_llm(datos_usuario)
            else:
                recomendaciones_llm = self._generar_fallback(datos_usuario)
            
            # Guardar recomendaciones en base de datos
            self._guardar_recomendaciones(usuario, recomendaciones_llm)
            
            return {
                'usuario': usuario.username,
                'total_cajones': datos_usuario['total_cajones'],
                'total_objetos': datos_usuario['total_objetos'],
                'recomendaciones': recomendaciones_llm,
                'generado_con_ia': self.client is not None
            }
            
        except User.DoesNotExist:
            logger.error(f"Usuario con ID {usuario_id} no encontrado")
            return {'error': 'Usuario no encontrado'}
        except Exception as e:
            logger.error(f"Error generando recomendaciones para usuario {usuario_id}: {str(e)}")
            return {'error': f'Error interno: {str(e)}'}
    
    def _recopilar_datos_usuario(self, usuario: User) -> Dict[str, Any]:
        """
        Recopila todos los datos necesarios del usuario para el análisis.
        
        Args:
            usuario: Instancia del usuario
            
        Returns:
            Dict con datos estructurados del usuario
        """
        cajones = Cajon.objects.filter(usuario=usuario, is_active=True)
        
        datos_cajones = []
        total_objetos = 0
        
        for cajon in cajones:
            objetos = Objeto.objects.filter(cajon=cajon, is_active=True)
            objetos_data = []
            
            for objeto in objetos:
                objetos_data.append({
                    'nombre': objeto.nombre,
                    'tipo': objeto.tipo_objeto,
                    'tamanio': objeto.tamanio,
                    'descripcion': objeto.descripcion or '',
                    'fecha_ingreso': objeto.fecha_ingreso.isoformat()
                })
            
            total_objetos += len(objetos_data)
            
            # Estadísticas por tipo de objeto
            tipos_objetos = {}
            for obj in objetos_data:
                tipo = obj['tipo']
                tipos_objetos[tipo] = tipos_objetos.get(tipo, 0) + 1
            
            # Estadísticas por tamaño
            tamanios_objetos = {}
            for obj in objetos_data:
                tamanio = obj['tamanio']
                tamanios_objetos[tamanio] = tamanios_objetos.get(tamanio, 0) + 1
            
            datos_cajones.append({
                'nombre': cajon.nombre,
                'capacidad_maxima': cajon.capacidad_maxima,
                'objetos_actuales': len(objetos_data),
                'capacidad_disponible': cajon.capacidad_disponible,
                'porcentaje_ocupacion': cajon.porcentaje_uso,
                'objetos': objetos_data,
                'tipos_objetos': tipos_objetos,
                'tamanios_objetos': tamanios_objetos,
                'descripcion': cajon.descripcion or ''
            })
        
        return {
            'usuario': usuario.username,
            'total_cajones': len(datos_cajones),
            'total_objetos': total_objetos,
            'cajones': datos_cajones
        }
    
    def _generar_con_llm(self, datos_usuario: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Genera recomendaciones usando el LLM de OpenAI.
        
        Args:
            datos_usuario: Datos estructurados del usuario
            
        Returns:
            Lista de recomendaciones generadas por el LLM
        """
        try:
            # Construir el prompt para el LLM
            prompt = self._construir_prompt(datos_usuario)
            
            # Llamar al LLM
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un experto organizador personal especializado en optimización de espacios y cajones. Tu trabajo es analizar la organización actual de objetos en cajones y generar recomendaciones prácticas y específicas."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            # Parsear la respuesta
            contenido_respuesta = response.choices[0].message.content
            
            # Intentar parsear como JSON, si no es posible, crear estructura manual
            try:
                recomendaciones = json.loads(contenido_respuesta)
                if isinstance(recomendaciones, dict) and 'recomendaciones' in recomendaciones:
                    return recomendaciones['recomendaciones']
                elif isinstance(recomendaciones, list):
                    return recomendaciones
            except json.JSONDecodeError:
                # Si no es JSON válido, parsear manualmente
                return self._parsear_respuesta_texto(contenido_respuesta)
            
        except Exception as e:
            logger.error(f"Error llamando al LLM: {str(e)}")
            return self._generar_fallback(datos_usuario)
    
    def _construir_prompt(self, datos_usuario: Dict[str, Any]) -> str:
        """
        Construye el prompt para el LLM basado en los datos del usuario.
        
        Args:
            datos_usuario: Datos del usuario
            
        Returns:
            Prompt estructurado para el LLM
        """
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
    
    def _parsear_respuesta_texto(self, contenido: str) -> List[Dict[str, Any]]:
        """
        Parsea una respuesta de texto cuando no es JSON válido.
        
        Args:
            contenido: Contenido de texto de la respuesta
            
        Returns:
            Lista de recomendaciones parseadas
        """
        # Implementación básica de parseo de texto
        recomendaciones = []
        lineas = contenido.split('\n')
        
        recomendacion_actual = None
        
        for linea in lineas:
            linea = linea.strip()
            if not linea:
                continue
                
            # Detectar inicio de nueva recomendación
            if any(keyword in linea.lower() for keyword in ['recomendación', 'sugerencia', 'consejo', '1.', '2.', '3.', '4.', '5.']):
                if recomendacion_actual:
                    recomendaciones.append(recomendacion_actual)
                
                recomendacion_actual = {
                    'titulo': linea,
                    'descripcion': '',
                    'tipo': 'ORGANIZACION',
                    'prioridad': 'MEDIA',
                    'razon': 'Recomendación generada por análisis automático'
                }
            elif recomendacion_actual:
                recomendacion_actual['descripcion'] += linea + ' '
        
        # Agregar la última recomendación
        if recomendacion_actual:
            recomendaciones.append(recomendacion_actual)
        
        return recomendaciones[:5]  # Máximo 5 recomendaciones
    
    def _generar_fallback(self, datos_usuario: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Genera recomendaciones básicas cuando no está disponible el LLM.
        
        Args:
            datos_usuario: Datos del usuario
            
        Returns:
            Lista de recomendaciones básicas
        """
        recomendaciones = []
        
        # Analizar cajones sobrecargados
        for cajon in datos_usuario['cajones']:
            if cajon['porcentaje_ocupacion'] > 90:
                recomendaciones.append({
                    'titulo': f"Cajón '{cajon['nombre']}' está sobrecargado",
                    'descripcion': f"El cajón tiene {cajon['objetos_actuales']} objetos de {cajon['capacidad_maxima']} posibles. Considera redistribuir algunos objetos a otros cajones.",
                    'tipo': 'ESPACIO',
                    'prioridad': 'ALTA',
                    'razon': 'Un cajón sobrecargado dificulta encontrar objetos y puede causar desorganización.'
                })
            elif cajon['porcentaje_ocupacion'] < 30:
                recomendaciones.append({
                    'titulo': f"Cajón '{cajon['nombre']}' está subutilizado",
                    'descripcion': f"Este cajón solo tiene {cajon['objetos_actuales']} objetos y puede almacenar {cajon['capacidad_maxima']}. Podrías mover objetos de otros cajones aquí.",
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
            recomendaciones.append({
                'titulo': 'Organizar objetos por categorías',
                'descripcion': 'Algunos cajones tienen muchos tipos diferentes de objetos mezclados. Considera agrupar objetos similares en el mismo cajón.',
                'tipo': 'ORGANIZACION',
                'prioridad': 'MEDIA',
                'razon': 'Agrupar objetos por tipo facilita encontrarlos y mantiene mejor orden.'
            })
        
        # Recomendación general de mantenimiento
        if datos_usuario['total_objetos'] > 20:
            recomendaciones.append({
                'titulo': 'Revisión periódica de objetos',
                'descripcion': 'Con muchos objetos almacenados, es recomendable hacer una revisión mensual para eliminar objetos que ya no necesitas.',
                'tipo': 'MANTENIMIENTO',
                'prioridad': 'BAJA',
                'razon': 'El mantenimiento regular previene la acumulación innecesaria y mantiene la organización.'
            })
        
        return recomendaciones[:5]  # Máximo 5 recomendaciones
    
    def _guardar_recomendaciones(self, usuario: User, recomendaciones: List[Dict[str, Any]]) -> None:
        """
        Guarda las recomendaciones generadas en la base de datos.
        
        Args:
            usuario: Usuario destinatario
            recomendaciones: Lista de recomendaciones a guardar
        """
        for rec in recomendaciones:
            try:
                Recomendacion.objects.create(
                    nombre=rec.get('titulo', 'Recomendación sin título'),
                    descripcion=rec.get('descripcion', '') + f"\n\nRazón: {rec.get('razon', '')}",
                    usuario=usuario,
                    tipo_recomendacion=rec.get('tipo', 'ORGANIZACION'),
                    prioridad=rec.get('prioridad', 'MEDIA')
                )
            except Exception as e:
                logger.error(f"Error guardando recomendación: {str(e)}")
