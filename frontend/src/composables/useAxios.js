import axios from 'axios';
import { ref } from 'vue';

// Create a configured axios instance
const api = axios.create({
  baseURL: 'http://127.0.0.1:5000/',
  headers: {
    'Content-Type': 'application/json',
  }
});

// Add interceptor to include Bearer token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers["Authorization"] = `Bearer ${token}`;  
  }
  return config;
});

export function useAxios() {
  const loading = ref(false);
  const error = ref(null);

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
