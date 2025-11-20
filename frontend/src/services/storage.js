/**
 * Local storage utilities
 */

const STORAGE_KEYS = {
  USER: 'cititrack_user',
  TOKEN: 'cititrack_token',
  LANGUAGE: 'cititrack_language',
  THEME: 'cititrack_theme',
  LAST_LOCATION: 'cititrack_last_location',
};

export const storage = {
  // User
  setUser(user) {
    localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(user));
  },

  getUser() {
    const user = localStorage.getItem(STORAGE_KEYS.USER);
    return user ? JSON.parse(user) : null;
  },

  clearUser() {
    localStorage.removeItem(STORAGE_KEYS.USER);
  },

  // Token
  setToken(token) {
    localStorage.setItem(STORAGE_KEYS.TOKEN, token);
  },

  getToken() {
    return localStorage.getItem(STORAGE_KEYS.TOKEN);
  },

  clearToken() {
    localStorage.removeItem(STORAGE_KEYS.TOKEN);
  },

  // Language
  setLanguage(language) {
    localStorage.setItem(STORAGE_KEYS.LANGUAGE, language);
  },

  getLanguage() {
    return localStorage.getItem(STORAGE_KEYS.LANGUAGE) || 'en';
  },

  // Theme
  setTheme(theme) {
    localStorage.setItem(STORAGE_KEYS.THEME, theme);
  },

  getTheme() {
    return localStorage.getItem(STORAGE_KEYS.THEME) || 'light';
  },

  // Last location
  setLastLocation(location) {
    localStorage.setItem(STORAGE_KEYS.LAST_LOCATION, JSON.stringify(location));
  },

  getLastLocation() {
    const location = localStorage.getItem(STORAGE_KEYS.LAST_LOCATION);
    return location ? JSON.parse(location) : null;
  },

  // Clear all
  clearAll() {
    Object.values(STORAGE_KEYS).forEach(key => {
      localStorage.removeItem(key);
    });
  },
};

export default storage;