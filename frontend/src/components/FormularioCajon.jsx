import React, { useState, useEffect } from 'react';
import { cajonService } from '../services/cajonService';
import { toast } from 'react-toastify';

const FormularioCajon = ({ cajon = null, onSuccess, onCancel }) => {
  const [formData, setFormData] = useState({
    nombre: '',
    capacidad_maxima: 10,
    descripcion: ''
  });
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});

  useEffect(() => {
    if (cajon) {
      setFormData({
        nombre: cajon.nombre || '',
        capacidad_maxima: cajon.capacidad_maxima || 10,
        descripcion: cajon.descripcion || ''
      });
    }
  }, [cajon]);

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.nombre.trim()) {
      newErrors.nombre = 'El nombre es obligatorio';
    } else if (formData.nombre.length > 100) {
      newErrors.nombre = 'El nombre no puede exceder 100 caracteres';
    } else if (!/^[a-zA-Z0-9\s]+$/.test(formData.nombre)) {
      newErrors.nombre = 'Solo se permiten letras, números y espacios';
    }

    if (!formData.capacidad_maxima || formData.capacidad_maxima < 1) {
      newErrors.capacidad_maxima = 'La capacidad debe ser al menos 1';
    } else if (formData.capacidad_maxima > 1000) {
      newErrors.capacidad_maxima = 'La capacidad no puede exceder 1000';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'capacidad_maxima' ? parseInt(value) || 0 : value
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
      let resultado;
      if (cajon) {
        // Actualizar cajón existente
        resultado = await cajonService.updateCajon(cajon.id, formData);
        toast.success('Cajón actualizado exitosamente');
      } else {
        // Crear nuevo cajón
        resultado = await cajonService.createCajon(formData);
        toast.success('Cajón creado exitosamente');
      }
      
      if (onSuccess) {
        onSuccess(resultado);
      }
    } catch (error) {
      toast.error(error.message || 'Error al guardar el cajón');
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">
        {cajon ? 'Editar Cajón' : 'Crear Nuevo Cajón'}
      </h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Nombre */}
        <div>
          <label htmlFor="nombre" className="block text-sm font-medium text-gray-700 mb-1">
            Nombre del Cajón *
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
            placeholder="Ingresa el nombre del cajón"
            maxLength={100}
          />
          {errors.nombre && (
            <p className="mt-1 text-sm text-red-600">{errors.nombre}</p>
          )}
        </div>

        {/* Capacidad Máxima */}
        <div>
          <label htmlFor="capacidad_maxima" className="block text-sm font-medium text-gray-700 mb-1">
            Capacidad Máxima *
          </label>
          <input
            type="number"
            id="capacidad_maxima"
            name="capacidad_maxima"
            value={formData.capacidad_maxima}
            onChange={handleChange}
            min="1"
            max="1000"
            className={`w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-orange-500 focus:border-orange-500 ${
              errors.capacidad_maxima ? 'border-red-500' : 'border-gray-300'
            }`}
            placeholder="Número máximo de objetos"
          />
          {errors.capacidad_maxima && (
            <p className="mt-1 text-sm text-red-600">{errors.capacidad_maxima}</p>
          )}
          <p className="mt-1 text-xs text-gray-500">
            Número máximo de objetos que puede contener el cajón (1-1000)
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
            placeholder="Descripción adicional del cajón"
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
              cajon ? 'Actualizar Cajón' : 'Crear Cajón'
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default FormularioCajon;
