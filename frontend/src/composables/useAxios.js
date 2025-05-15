import axios from 'axios';
import { ref } from 'vue';

// Create a configured axios instance
const api = axios.create({
  baseURL: 'http://127.0.0.1:5000/api',
  headers: {
    'Content-Type': 'application/json',
  }
});

// Add interceptor to include auth token in requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers["Authentication-Token"] = token;
  }
  return config;
});

export function useAxios() {
  const loading = ref(false);
  const error = ref(null);

  // GET request with error handling
  const get = async (url, config = {}) => {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await api.get(url, config);
      return response.data;
    } catch (err) {
      error.value = err.response?.data?.message || 'An error occurred';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // POST request with error handling
  const post = async (url, data = {}, config = {}) => {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await api.post(url, data, config);
      return response.data;
    } catch (err) {
      error.value = err.response?.data?.message || 'An error occurred';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // PUT request with error handling
  const put = async (url, data = {}, config = {}) => {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await api.put(url, data, config);
      return response.data;
    } catch (err) {
      error.value = err.response?.data?.message || 'An error occurred';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // DELETE request with error handling
  const del = async (url, config = {}) => {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await api.delete(url, config);
      return response.data;
    } catch (err) {
      error.value = err.response?.data?.message || 'An error occurred';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  return {
    get,
    post,
    put,
    del,
    loading,
    error,
    api
  };
}

export default api; 