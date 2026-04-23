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

export function getApiBaseUrl() {
  return (import.meta.env.VITE_API_BASE_URL || getDefaultApiBaseUrl()).replace(/\/$/, '');
}

export async function apiRequest(path, options = {}) {
  const { body, headers, ...restOptions } = options;
  const isFormData = typeof FormData !== 'undefined' && body instanceof FormData;

  let response;

  try {
    response = await fetch(`${getApiBaseUrl()}${path}`, {
      credentials: 'include',
      headers: {
        ...(body && !isFormData ? { 'Content-Type': 'application/json' } : {}),
        ...headers,
      },
      body: body ? (isFormData ? body : JSON.stringify(body)) : undefined,
      ...restOptions,
    });
  } catch {
    const error = new Error(
      'Unable to reach the backend. Make sure the Flask server is running.',
    );
    error.status = 0;
    throw error;
  }

  const responseText = await response.text();
  const responseData = responseText ? JSON.parse(responseText) : {};
  const firstFieldError = responseData.errors
    ? Object.values(responseData.errors).find((value) => typeof value === 'string')
    : '';

  if (!response.ok) {
    const error = new Error(
      responseData.error
      || responseData.message
      || responseData.errors?.general
      || firstFieldError
      || 'Request failed.',
    );
    error.status = response.status;
    error.data = responseData;
    throw error;
  }

  return responseData;
}
