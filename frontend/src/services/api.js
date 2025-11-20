import axios from 'axios';
import { offlineQueue } from './offline';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add auth token if exists
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (!error.response) {
      // Network error - queue for offline
      console.log('Network error, queuing request');
    }
    return Promise.reject(error);
  }
);

// API methods
export const reportsAPI = {
  // Create report
  async create(reportData) {
    try {
      const response = await api.post('/api/reports', reportData);
      return { success: true, data: response.data };
    } catch (error) {
      if (!navigator.onLine) {
        // Queue for offline submission
        await offlineQueue.addReport(reportData);
        return { success: true, queued: true, data: { id: 'PENDING' } };
      }
      return { success: false, error: error.message };
    }
  },

  // Get all reports
  async getAll(params = {}) {
    const response = await api.get('/api/reports', { params });
    return response.data;
  },

  // Get single report
  async getById(id) {
    const response = await api.get(`/api/reports/${id}`);
    return response.data;
  },

  // Update report
  async update(id, data) {
    const response = await api.patch(`/api/reports/${id}`, data);
    return response.data;
  },

  // Resolve report
  async resolve(id) {
    const response = await api.post(`/api/reports/${id}/resolve`);
    return response.data;
  },

  // Upvote report
  async upvote(id) {
    const response = await api.post(`/api/reports/${id}/upvote`);
    return response.data;
  },

  // Upload photo
  async uploadPhoto(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post('/api/reports/upload-photo', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },
};

export const dashboardAPI = {
  // Get dashboard stats
  async getStats() {
    const response = await api.get('/api/dashboard/stats');
    return response.data;
  },

  // Get recent reports
  async getRecent(limit = 10) {
    const response = await api.get('/api/dashboard/recent', {
      params: { limit },
    });
    return response.data;
  },

  // Get trending issues
  async getTrending() {
    const response = await api.get('/api/dashboard/trending');
    return response.data;
  },
};

export const blockchainAPI = {
  // Verify report on blockchain
  async verify(reportId) {
    const response = await api.get(`/api/blockchain/verify/${reportId}`);
    return response.data;
  },

  // Get blockchain status
  async getStatus() {
    const response = await api.get('/api/blockchain/status');
    return response.data;
  },

  // Get transaction info
  async getTransaction(txHash) {
    const response = await api.get(`/api/blockchain/transaction/${txHash}`);
    return response.data;
  },
};

export const authAPI = {
  // Register
  async register(userData) {
    const response = await api.post('/api/auth/register', userData);
    return response.data;
  },

  // Login
  async login(email, password) {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);
    
    const response = await api.post('/api/auth/token', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    
    // Save token
    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token);
    }
    
    return response.data;
  },

  // Get current user
  async getMe() {
    const response = await api.get('/api/auth/me');
    return response.data;
  },

  // Logout
  logout() {
    localStorage.removeItem('token');
  },
};

export default api;