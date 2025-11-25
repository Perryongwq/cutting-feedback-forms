/**
 * API service layer for communicating with Flask backend.
 */
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add any auth tokens here if needed in future
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle common errors
    if (error.response) {
      // Server responded with error status
      const { status, data } = error.response;
      if (status === 400) {
        // Validation error
        return Promise.reject(new Error(data.message || 'Validation failed'));
      } else if (status === 500) {
        return Promise.reject(new Error('Server error. Please try again later.'));
      }
    } else if (error.request) {
      // Request made but no response
      return Promise.reject(new Error('Network error. Please check your connection.'));
    }
    return Promise.reject(error);
  }
);

/**
 * Submit A1 cutting process feedback form.
 * @param {FormData} formData - Form data with files
 * @returns {Promise} API response
 */
export const submitA1Form = (formData) => {
  return api.post('/a1/submit', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

/**
 * Submit GHM cutting process feedback form.
 * @param {FormData} formData - Form data with files
 * @returns {Promise} API response
 */
export const submitGHMForm = (formData) => {
  return api.post('/ghm/submit', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

/**
 * Submit KEM cutting process feedback form.
 * @param {FormData} formData - Form data with files
 * @returns {Promise} API response
 */
export const submitKEMForm = (formData) => {
  return api.post('/kem/submit', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

/**
 * Get A1 feedback history.
 * @returns {Promise} API response with history data
 */
export const getA1History = () => {
  return api.get('/a1/history');
};

/**
 * Get GHM feedback history.
 * @returns {Promise} API response with history data
 */
export const getGHMHistory = () => {
  return api.get('/ghm/history');
};

/**
 * Get KEM feedback history.
 * @returns {Promise} API response with history data
 */
export const getKEMHistory = () => {
  return api.get('/kem/history');
};

/**
 * Download A1 history as Excel file.
 * @returns {Promise} Blob response
 */
export const downloadA1History = async () => {
  const response = await api.get('/a1/history/download', {
    responseType: 'blob',
  });
  return response.data;
};

/**
 * Download GHM history as Excel file.
 * @returns {Promise} Blob response
 */
export const downloadGHMHistory = async () => {
  const response = await api.get('/ghm/history/download', {
    responseType: 'blob',
  });
  return response.data;
};

/**
 * Download KEM history as Excel file.
 * @returns {Promise} Blob response
 */
export const downloadKEMHistory = async () => {
  const response = await api.get('/kem/history/download', {
    responseType: 'blob',
  });
  return response.data;
};

export default api;



