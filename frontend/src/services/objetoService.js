import api from '../utils/api';

// Servicio para gestión de objetos
export const objetoService = {
  // Obtener todos los objetos
  async getObjetos(params = {}) {
    try {
      const response = await api.get('/objetos/', { params });
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  },

  // Obtener objetos por cajón
  async getObjetosByCajon(cajonId) {
    try {
      const response = await api.get('/objetos/', { 
        params: { cajon: cajonId } 
      });
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  },

  // Obtener un objeto específico
  async getObjeto(id) {
    try {
      const response = await api.get(`/objetos/${id}/`);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  },

  // Crear un nuevo objeto
  async createObjeto(objetoData) {
    try {
      const response = await api.post('/objetos/', objetoData);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  },

  // Actualizar un objeto
  async updateObjeto(id, objetoData) {
    try {
      const response = await api.put(`/objetos/${id}/`, objetoData);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  },

  // Eliminar un objeto
  async deleteObjeto(id) {
    try {
      await api.delete(`/objetos/${id}/`);
      return true;
    } catch (error) {
      throw this.handleError(error);
    }
  },

  // Buscar objetos
  async buscarObjetos(query) {
    try {
      const response = await api.get('/objetos/buscar/', { 
        params: { q: query } 
      });
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  },

  // Mover objeto a otro cajón
  async moverObjeto(objetoId, nuevoCajonId) {
    try {
      const response = await api.post(`/objetos/${objetoId}/mover/`, { 
        cajon: nuevoCajonId 
      });
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  },

  // Obtener tipos de objeto disponibles
  async getTiposObjeto() {
    try {
      const response = await api.get('/configuracion/tipos-objeto/');
      return response.data;
    } catch (error) {
      // Valores por defecto si no hay endpoint
      return [
        { value: 'ROPA', label: 'Ropa' },
        { value: 'PAPELERIA', label: 'Papelería' },
        { value: 'CABLES', label: 'Cables' },
        { value: 'ELECTRONICA', label: 'Electrónica' },
        { value: 'LIBROS', label: 'Libros' },
        { value: 'HERRAMIENTAS', label: 'Herramientas' },
        { value: 'COCINA', label: 'Artículos de Cocina' },
        { value: 'OTROS', label: 'Otros' }
      ];
    }
  },

  // Obtener tamaños disponibles
  async getTamanios() {
    try {
      const response = await api.get('/configuracion/tamanios/');
      return response.data;
    } catch (error) {
      // Valores por defecto si no hay endpoint
      return [
        { value: 'PEQUENO', label: 'Pequeño' },
        { value: 'MEDIANO', label: 'Mediano' },
        { value: 'GRANDE', label: 'Grande' }
      ];
    }
  },

  handleError(error) {
    if (error.response?.data?.detail) {
      return new Error(error.response.data.detail);
    }
    if (error.response?.data?.message) {
      return new Error(error.response.data.message);
    }
    if (error.response?.data) {
      // Manejar errores de validación
      const errorMessages = Object.values(error.response.data).flat();
      return new Error(errorMessages.join(', '));
    }
    return new Error('Error al comunicarse con el servidor');
  }
};
