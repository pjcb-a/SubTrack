const DEFAULT_API_BASE_URL = 'http://127.0.0.1:5000';

function getApiBaseUrl() {
  return (import.meta.env.VITE_API_BASE_URL || DEFAULT_API_BASE_URL).replace(/\/$/, '');
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
