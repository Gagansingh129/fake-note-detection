/**
 * NoteGuard AI - Centralized API Service
 * =====================================
 * Single source of truth for all HTTP communications between
 * the React frontend and the FastAPI backend.
 */

// Empty string default uses relative paths so Nginx reverse-proxies seamlessly in production & Docker
const API_BASE_URL = (import.meta.env.VITE_API_URL !== undefined && import.meta.env.VITE_API_URL !== '')
  ? import.meta.env.VITE_API_URL
  : '';

export const resolveImageUrl = (path) => {
  if (!path) return '';
  if (path.startsWith('http://') || path.startsWith('https://')) return path;
  const cleanPath = path.startsWith('/') ? path : `/${path}`;
  return `${API_BASE_URL}${cleanPath}`;
};

export const api = {
  /** Check server health and loaded model status */
  async checkHealth() {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);
      if (!response.ok) throw new Error(`Health check failed: ${response.statusText}`);
      return await response.json();
    } catch (err) {
      console.error('[API Health Error]:', err);
      return { status: 'offline', error: err.message };
    }
  },

  /** Upload image file for authenticity screening */
  async predictImage(file) {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_BASE_URL}/api/predict`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `Screening request failed with status ${response.status}`);
    }

    return await response.json();
  },

  /** Send live webcam captured base64 snapshot */
  async predictCamera(imageBase64) {
    const response = await fetch(`${API_BASE_URL}/api/predict/camera`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ image_base64: imageBase64 }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `Camera analysis failed with status ${response.status}`);
    }

    return await response.json();
  },

  /** Fetch past screening records with optional status filter */
  async getHistory(filterBy = null, limit = 50) {
    let url = `${API_BASE_URL}/api/history?limit=${limit}`;
    if (filterBy && filterBy !== 'all') {
      url += `&filter_by=${encodeURIComponent(filterBy)}`;
    }

    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Failed to retrieve history: ${response.statusText}`);
    }

    return await response.json();
  },

  /** Delete a specific audit history record */
  async deleteHistory(recordId) {
    const response = await fetch(`${API_BASE_URL}/api/history/${recordId}`, {
      method: 'DELETE',
    });

    if (!response.ok) {
      throw new Error(`Failed to delete record: ${response.statusText}`);
    }

    return await response.json();
  },
};
