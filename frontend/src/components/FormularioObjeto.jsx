import React, { useState, useEffect } from 'react';
import { objetoService } from '../services/objetoService';
import { cajonService } from '../services/cajonService';
import { toast } from 'react-toastify';

const FormularioObjeto = ({ objeto = null, cajonPredeterminado = null, onSuccess, onCancel }) => {
  const [formData, setFormData] = useState({
    nombre: '',
    tipo_objeto: 'OTROS',
    tamanio: 'MEDIANO',
    cajon: '',
    descripcion: ''
  });
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});
  const [cajones, setCajones] = useState([]);
  const [tiposObjeto, setTiposObjeto] = useState([]);
  const [tamanios, setTamanios] = useState([]);

  useEffect(() => {
    // Cargar datos iniciales
    cargarDatosIniciales();
  }, []);

  useEffect(() => {
    if (objeto) {
      setFormData({
        nombre: objeto.nombre || '',
        tipo_objeto: objeto.tipo_objeto || 'OTROS',
        tamanio: objeto.tamanio || 'MEDIANO',
        cajon: objeto.cajon?.id || '',
        descripcion: objeto.descripcion || ''
      });
    } else if (cajonPredeterminado) {
      setFormData(prev => ({
        ...prev,
        cajon: cajonPredeterminado.id
      }));
    }
  }, [objeto, cajonPredeterminado]);

  const cargarDatosIniciales = async () => {
    try {
      const [cajonesData, tiposData, tamaniosData] = await Promise.all([
        cajonService.getCajones(),
        objetoService.getTiposObjeto(),
        objetoService.getTamanios()
      ]);
      
      setCajones(cajonesData.results || cajonesData);
      setTiposObjeto(tiposData);
      setTamanios(tamaniosData);
    } catch (error) {
      console.error('Error cargando datos iniciales:', error);
      toast.error('Error al cargar los datos del formulario');
    }
  };

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.nombre.trim()) {
      newErrors.nombre = 'El nombre es obligatorio';
    } else if (formData.nombre.length > 100) {
      newErrors.nombre = 'El nombre no puede exceder 100 caracteres';
    }

    if (!formData.tipo_objeto) {
      newErrors.tipo_objeto = 'Debe seleccionar un tipo de objeto';
    }

    if (!formData.tamanio) {
      newErrors.tamanio = 'Debe seleccionar un tamaño';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Limpiar error del campo cuando el usuario empieza a escribir
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setLoading(true);
    try {
      // Preparar datos para envío
      const dataToSend = { ...formData };
      if (!dataToSend.cajon) {
        delete dataToSend.cajon; // No enviar cajón si no está seleccionado
      }

      let resultado;
      if (objeto) {
        // Actualizar objeto existente
        resultado = await objetoService.updateObjeto(objeto.id, dataToSend);
        toast.success('Objeto actualizado exitosamente');
      } else {
        // Crear nuevo objeto
        resultado = await objetoService.createObjeto(dataToSend);
        toast.success('Objeto creado exitosamente');
      }
      
      if (onSuccess) {
        onSuccess(resultado);
      }
    } catch (error) {
      toast.error(error.message || 'Error al guardar el objeto');
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">
        {objeto ? 'Editar Objeto' : 'Crear Nuevo Objeto'}
      </h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Nombre */}
        <div>
          <label htmlFor="nombre" className="block text-sm font-medium text-gray-700 mb-1">
            Nombre del Objeto *
          </label>
          <input
            type="text"
            id="nombre"
            name="nombre"
            value={formData.nombre}
            onChange={handleChange}
            className={`w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-orange-500 focus:border-orange-500 ${
              errors.nombre ? 'border-red-500' : 'border-gray-300'
            }`}
            placeholder="Ingresa el nombre del objeto"
            maxLength={100}
          />
          {errors.nombre && (
            <p className="mt-1 text-sm text-red-600">{errors.nombre}</p>
          )}
        </div>

        {/* Tipo de Objeto */}
        <div>
          <label htmlFor="tipo_objeto" className="block text-sm font-medium text-gray-700 mb-1">
            Tipo de Objeto *
          </label>
          <select
            id="tipo_objeto"
            name="tipo_objeto"
            value={formData.tipo_objeto}
            onChange={handleChange}
            className={`w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-orange-500 focus:border-orange-500 ${
              errors.tipo_objeto ? 'border-red-500' : 'border-gray-300'
            }`}
          >
            {tiposObjeto.map((tipo) => (
              <option key={tipo.value} value={tipo.value}>
                {tipo.label}
              </option>
            ))}
          </select>
          {errors.tipo_objeto && (
            <p className="mt-1 text-sm text-red-600">{errors.tipo_objeto}</p>
          )}
        </div>

        {/* Tamaño */}
        <div>
          <label htmlFor="tamanio" className="block text-sm font-medium text-gray-700 mb-1">
            Tamaño *
          </label>
          <select
            id="tamanio"
            name="tamanio"
            value={formData.tamanio}
            onChange={handleChange}
            className={`w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-orange-500 focus:border-orange-500 ${
              errors.tamanio ? 'border-red-500' : 'border-gray-300'
            }`}
          >
            {tamanios.map((tamanio) => (
              <option key={tamanio.value} value={tamanio.value}>
                {tamanio.label}
              </option>
            ))}
          </select>
          {errors.tamanio && (
            <p className="mt-1 text-sm text-red-600">{errors.tamanio}</p>
          )}
        </div>

        {/* Cajón */}
        <div>
          <label htmlFor="cajon" className="block text-sm font-medium text-gray-700 mb-1">
            Cajón (Opcional)
          </label>
          <select
            id="cajon"
            name="cajon"
            value={formData.cajon}
            onChange={handleChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-orange-500 focus:border-orange-500"
          >
            <option value="">Sin asignar</option>
            {cajones.map((cajon) => (
              <option key={cajon.id} value={cajon.id}>
                {cajon.nombre} ({cajon.objetos_count || 0}/{cajon.capacidad_maxima})
              </option>
            ))}
          </select>
          <p className="mt-1 text-xs text-gray-500">
            Selecciona un cajón para almacenar el objeto
          </p>
        </div>

        {/* Descripción */}
        <div>
          <label htmlFor="descripcion" className="block text-sm font-medium text-gray-700 mb-1">
            Descripción (Opcional)
          </label>
          <textarea
            id="descripcion"
            name="descripcion"
            value={formData.descripcion}
            onChange={handleChange}
            rows={3}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-orange-500 focus:border-orange-500"
            placeholder="Descripción adicional del objeto"
          />
        </div>

        {/* Botones */}
        <div className="flex justify-end space-x-3 pt-4">
          <button
            type="button"
            onClick={onCancel}
            className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-orange-500"
          >
            Cancelar
          </button>
          <button
            type="submit"
            disabled={loading}
            className="px-4 py-2 bg-orange-600 border border-transparent rounded-md text-sm font-medium text-white hover:bg-orange-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-orange-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <div className="flex items-center">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                Guardando...
              </div>
            ) : (
              objeto ? 'Actualizar Objeto' : 'Crear Objeto'
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default FormularioObjeto;
