const DEFAULT_API_PORT = '5000';
const FALLBACK_API_BASE_URL = 'http://127.0.0.1:5000';

function getDefaultApiBaseUrl() {
  if (typeof window === 'undefined') {
    return FALLBACK_API_BASE_URL;
  }

  const { protocol, hostname } = window.location;

  // Keep the backend host aligned with the page host so Flask's session cookie
  // is treated as first-party in local development regardless of whether the
  // app is opened through localhost, 127.0.0.1, or a LAN IP.
  if (hostname) {
    return `${protocol}//${hostname}:${DEFAULT_API_PORT}`;
  }

  return FALLBACK_API_BASE_URL;
}

function getApiBaseUrl() {
  return (import.meta.env.VITE_API_BASE_URL || getDefaultApiBaseUrl()).replace(/\/$/, '');
}

export async function apiRequest(path, options = {}) {
  const { body, headers, ...restOptions } = options;

  const response = await fetch(`${getApiBaseUrl()}${path}`, {
    credentials: 'include',
    headers: {
      ...(body ? { 'Content-Type': 'application/json' } : {}),
      ...headers,
    },
    body: body ? JSON.stringify(body) : undefined,
    ...restOptions,
  });

  const responseText = await response.text();
  const responseData = responseText ? JSON.parse(responseText) : {};

  if (!response.ok) {
    const error = new Error(
      responseData.error
      || responseData.message
      || responseData.errors?.general
      || 'Request failed.',
    );
    error.status = response.status;
    error.data = responseData;
    throw error;
  }

  return responseData;
}
