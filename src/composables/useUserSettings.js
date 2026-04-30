import { ref } from 'vue';
import { apiRequest, buildBackendUnavailableError, getApiBaseUrl } from '../lib/api';
import { useAuth } from './useAuth';
import { useSubscriptions } from './useSubscriptions';

const settings = ref(null);
const capStatus = ref(null);
const settingsLoading = ref(false);
const settingsSaving = ref(false);
const settingsError = ref('');
const importResult = ref(null);

let settingsPromise = null;

function applySettingsPayload(payload) {
  const { currentUser } = useAuth();

  if (payload.user) {
    currentUser.value = payload.user;
  }

  settings.value = payload.settings ?? settings.value;
  capStatus.value = payload.cap_status ?? capStatus.value;
}

async function fetchSettings(force = false) {
  if (settingsPromise && !force) {
    return settingsPromise;
  }

  settingsLoading.value = true;
  settingsError.value = '';

  settingsPromise = (async () => {
    try {
      const response = await apiRequest('/api/user/settings');
      applySettingsPayload(response);
      return response;
    } catch (error) {
      settingsError.value = error.message;
      throw error;
    } finally {
      settingsLoading.value = false;
      settingsPromise = null;
    }
  })();

  return settingsPromise;
}

async function updateProfile(username) {
  settingsSaving.value = true;
  settingsError.value = '';

  try {
    const response = await apiRequest('/api/user/profile', {
      method: 'PATCH',
      body: { username },
    });
    applySettingsPayload({ user: response.user });
    return response;
  } catch (error) {
    settingsError.value = error.message;
    throw error;
  } finally {
    settingsSaving.value = false;
  }
}

async function changePassword(payload) {
  settingsSaving.value = true;
  settingsError.value = '';

  try {
    return await apiRequest('/api/user/change-password', {
      method: 'POST',
      body: payload,
    });
  } catch (error) {
    settingsError.value = error.message;
    throw error;
  } finally {
    settingsSaving.value = false;
  }
}

async function updateSettings(payload) {
  settingsSaving.value = true;
  settingsError.value = '';

  try {
    const response = await apiRequest('/api/user/settings', {
      method: 'PATCH',
      body: payload,
    });
    applySettingsPayload(response);
    return response;
  } catch (error) {
    settingsError.value = error.message;
    throw error;
  } finally {
    settingsSaving.value = false;
  }
}

async function exportSubscriptionsCsv() {
  settingsSaving.value = true;
  settingsError.value = '';

  try {
    let response;

    try {
      response = await fetch(`${getApiBaseUrl()}/api/user/export`, {
        credentials: 'include',
      });
    } catch {
      throw buildBackendUnavailableError();
    }

    if (!response.ok) {
      let responseData = {};

      try {
        responseData = await response.json();
      } catch {
        responseData = {};
      }

      throw new Error(responseData.error || 'Export failed.');
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const anchor = document.createElement('a');
    anchor.href = url;
    anchor.download = 'subtrack-subscriptions.csv';
    document.body.appendChild(anchor);
    anchor.click();
    anchor.remove();
    window.URL.revokeObjectURL(url);
  } catch (error) {
    settingsError.value = error.message;
    throw error;
  } finally {
    settingsSaving.value = false;
  }
}

async function importSubscriptionsCsv(file) {
  if (!file) {
    throw new Error('Please choose a CSV file to import.');
  }

  settingsSaving.value = true;
  settingsError.value = '';
  const { fetchSubscriptions } = useSubscriptions();
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await apiRequest('/api/user/import', {
      method: 'POST',
      body: formData,
    });
    importResult.value = response.result;
    await fetchSubscriptions({ force: true });
    return response.result;
  } catch (error) {
    settingsError.value = error.message;
    throw error;
  } finally {
    settingsSaving.value = false;
  }
}

async function deleteAccount() {
  settingsSaving.value = true;
  settingsError.value = '';
  const { currentUser } = useAuth();
  const { resetSubscriptionStore } = useSubscriptions();

  try {
    const response = await apiRequest('/api/user/account', {
      method: 'DELETE',
    });
    currentUser.value = null;
    settings.value = null;
    capStatus.value = null;
    importResult.value = null;
    resetSubscriptionStore();
    return response;
  } catch (error) {
    settingsError.value = error.message;
    throw error;
  } finally {
    settingsSaving.value = false;
  }
}

function clearImportResult() {
  importResult.value = null;
}

export function useUserSettings() {
  return {
    settings,
    capStatus,
    settingsLoading,
    settingsSaving,
    settingsError,
    importResult,
    fetchSettings,
    updateProfile,
    changePassword,
    updateSettings,
    exportSubscriptionsCsv,
    importSubscriptionsCsv,
    deleteAccount,
    clearImportResult,
  };
}
