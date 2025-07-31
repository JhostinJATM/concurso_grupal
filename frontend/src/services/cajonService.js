import api from '../utils/api';

// Servicio para gestión de cajones
export const cajonService = {
  // Obtener todos los cajones del usuario
  async getCajones() {
    try {
      const response = await api.get('/cajones/');
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  },

  // Obtener un cajón específico
  async getCajon(id) {
    try {
      const response = await api.get(`/cajones/${id}/`);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  },

  // Crear un nuevo cajón
  async createCajon(cajonData) {
    try {
      const response = await api.post('/cajones/', cajonData);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  },

  // Actualizar un cajón
  async updateCajon(id, cajonData) {
    try {
      const response = await api.put(`/cajones/${id}/`, cajonData);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  },

  // Eliminar un cajón
  async deleteCajon(id) {
    try {
      await api.delete(`/cajones/${id}/`);
      return true;
    } catch (error) {
      throw this.handleError(error);
    }
  },

  // Obtener estadísticas del cajón
  async getEstadisticas(id) {
    try {
      const response = await api.get(`/cajones/${id}/estadisticas/`);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  },

  // Optimizar cajón
  async optimizarCajon(id) {
    try {
      const response = await api.post(`/cajones/${id}/optimizar/`);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
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
