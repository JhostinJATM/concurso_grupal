import api from '../utils/api';

// Servicio de autenticación
export const authService = {
  // Iniciar sesión
  async login(credentials) {
    try {
      const response = await api.post('/auth/login/', credentials);
      if (response.data.token) {
        localStorage.setItem('authToken', response.data.token);
        localStorage.setItem('user', JSON.stringify(response.data.user));
      }
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  },

  // Cerrar sesión
  async logout() {
    try {
      await api.post('/auth/logout/');
    } catch (error) {
      // Ignorar errores al cerrar sesión
    } finally {
      localStorage.removeItem('authToken');
      localStorage.removeItem('user');
    }
  },

  // Registrar usuario
  async register(userData) {
    try {
      const response = await api.post('/auth/register/', userData);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  },

  // Verificar si el usuario está autenticado
  isAuthenticated() {
    const token = localStorage.getItem('authToken');
    return !!token;
  },

  // Obtener usuario actual
  getCurrentUser() {
    const userString = localStorage.getItem('user');
    return userString ? JSON.parse(userString) : null;
  },

  // Obtener token
  getToken() {
    return localStorage.getItem('authToken');
  },

  handleError(error) {
    if (error.response?.data?.detail) {
      return new Error(error.response.data.detail);
    }
    if (error.response?.data?.message) {
      return new Error(error.response.data.message);
    }
    if (error.response?.data) {
      const errorMessages = Object.values(error.response.data).flat();
      return new Error(errorMessages.join(', '));
    }
    return new Error('Error de autenticación');
  }
};
