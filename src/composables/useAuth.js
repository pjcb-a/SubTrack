import { ref } from 'vue';
import { apiRequest } from '../lib/api';

const currentUser = ref(null);
const authReady = ref(false);
const authLoading = ref(false);
const authError = ref('');

let restorePromise = null;

async function restoreSession(force = false) {
  if (authReady.value && !force) {
    return currentUser.value;
  }

  if (restorePromise && !force) {
    return restorePromise;
  }

  restorePromise = (async () => {
    try {
      const response = await apiRequest('/api/user');
      currentUser.value = response.user;
    } catch (error) {
      if (error.status !== 401) {
        throw error;
      }

      currentUser.value = null;
    } finally {
      authReady.value = true;
      restorePromise = null;
    }

    return currentUser.value;
  })();

  return restorePromise;
}

async function login({ identifier, password }) {
  authLoading.value = true;
  authError.value = '';

  try {
    const trimmedIdentifier = identifier.trim();
    const payload = trimmedIdentifier.includes('@')
      ? { email: trimmedIdentifier, password }
      : { username: trimmedIdentifier, password };
    const response = await apiRequest('/api/auth/login', {
      method: 'POST',
      body: payload,
    });

    currentUser.value = response.user;
    authReady.value = true;
    return response.user;
  } catch (error) {
    authError.value = error.message;
    throw error;
  } finally {
    authLoading.value = false;
  }
}

async function register({ username, email, password }) {
  authLoading.value = true;
  authError.value = '';

  try {
    await apiRequest('/api/auth/register', {
      method: 'POST',
      body: {
        username,
        email,
        password,
      },
    });

    return await login({ identifier: email, password });
  } catch (error) {
    authError.value = error.message;
    throw error;
  } finally {
    authLoading.value = false;
  }
}

async function logout() {
  authLoading.value = true;

  try {
    await apiRequest('/api/auth/logout', {
      method: 'POST',
    });
  } finally {
    currentUser.value = null;
    authReady.value = true;
    authLoading.value = false;
  }
}

export function useAuth() {
  return {
    currentUser,
    authReady,
    authLoading,
    authError,
    restoreSession,
    login,
    register,
    logout,
  };
}
