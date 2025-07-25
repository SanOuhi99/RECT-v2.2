import { fetcher } from './api';

export async function login(email, password) {
  return fetcher('/api/v1/auth/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      username: email,
      password,
    }),
  });
}

export async function signup(userData) {
  return fetcher('/api/v1/auth/signup', {
    method: 'POST',
    body: JSON.stringify(userData),
  });
}

export async function getCurrentUser() {
  return fetcher('/api/v1/auth/me');
}
export async function refreshToken() {
  const response = await api.post('/auth/refresh');
  if (response.data?.access_token) {
    localStorage.setItem('access_token', response.data.access_token);
  }
  return response;
}
