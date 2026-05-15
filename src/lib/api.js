const DEFAULT_API_PORT = (import.meta.env.VITE_API_PORT || '5001').trim();
const FALLBACK_API_BASE_URL = `http://127.0.0.1:${DEFAULT_API_PORT}`;
const LOCAL_PROXY_API_BASE_URL = '';
const LOCAL_HOSTNAMES = new Set(['127.0.0.1', 'localhost']);

function isLocalPageHost(hostname) {
  return LOCAL_HOSTNAMES.has(hostname);
}

function isLocalApiUrl(url) {
  try {
    const parsedUrl = new URL(url);
    return LOCAL_HOSTNAMES.has(parsedUrl.hostname);
  } catch {
    return false;
  }
}

function getDefaultApiBaseUrl() {
  if (typeof window === 'undefined') {
    return FALLBACK_API_BASE_URL;
  }

  const { protocol, hostname } = window.location;

  if (isLocalPageHost(hostname)) {
    return FALLBACK_API_BASE_URL;
  }

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
  } catch (err) {
  throw new Error("Cannot connect to backend. Make sure Flask is running on port 5001.");
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
