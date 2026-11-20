/**
 * NoteGuard AI - Client Authentication Service
 * ============================================
 * Manages user login, registration, demo sessions, and JWT/session tokens.
 */

const API_BASE_URL = (import.meta.env.VITE_API_URL !== undefined && import.meta.env.VITE_API_URL !== '')
  ? import.meta.env.VITE_API_URL
  : '';

const TOKEN_KEY = 'noteguard_auth_token';
const USER_KEY = 'noteguard_auth_user';

const listeners = new Set();

function notifyListeners(user) {
  listeners.forEach((callback) => callback(user));
}

export const auth = {
  subscribe(callback) {
    listeners.add(callback);
    return () => listeners.delete(callback);
  },

  getToken() {
    return localStorage.getItem(TOKEN_KEY);
  },

  getCurrentUser() {
    try {
      const stored = localStorage.getItem(USER_KEY);
      return stored ? JSON.parse(stored) : null;
    } catch {
      return null;
    }
  },

  isAuthenticated() {
    return Boolean(this.getToken() && this.getCurrentUser());
  },

  saveSession(token, user) {
    localStorage.setItem(TOKEN_KEY, token);
    localStorage.setItem(USER_KEY, JSON.stringify(user));
    notifyListeners(user);
  },

  clearSession() {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
    notifyListeners(null);
  },

  async login(usernameOrEmail, password) {
    const res = await fetch(`${API_BASE_URL}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username_or_email: usernameOrEmail,
        password: password,
      }),
    });

    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.detail || 'Login failed.');
    }

    this.saveSession(data.token, data.user);
    return data.user;
  },

  async register(username, email, password, fullName = '') {
    const res = await fetch(`${API_BASE_URL}/api/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username,
        email,
        password,
        full_name: fullName,
      }),
    });

    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.detail || 'Registration failed.');
    }

    this.saveSession(data.token, data.user);
    return data.user;
  },

  async loginDemo() {
    const res = await fetch(`${API_BASE_URL}/api/auth/demo`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    });

    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.detail || 'Demo login failed.');
    }

    this.saveSession(data.token, data.user);
    return data.user;
  },

  async fetchCurrentUser() {
    const token = this.getToken();
    if (!token) {
      this.clearSession();
      return null;
    }

    try {
      const res = await fetch(`${API_BASE_URL}/api/auth/me`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) {
        this.clearSession();
        return null;
      }
      const data = await res.json();
      this.saveSession(token, data.user);
      return data.user;
    } catch {
      return this.getCurrentUser();
    }
  },

  async logout() {
    const token = this.getToken();
    try {
      if (token) {
        await fetch(`${API_BASE_URL}/api/auth/logout`, {
          method: 'POST',
          headers: { Authorization: `Bearer ${token}` },
        });
      }
    } catch {
      // Ignore network errors on logout
    } finally {
      this.clearSession();
    }
  },
};

