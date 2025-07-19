import { createContext, useContext, useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { fetcher } from '../lib/api';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    async function loadUser() {
      const token = localStorage.getItem('token');
      if (token) {
        try {
          const userData = await fetcher('/api/v1/auth/me');
          setUser(userData);
        } catch (err) {
          localStorage.removeItem('token');
        }
      }
      setLoading(false);
    }
    loadUser();
  }, []);

  const login = async (email, password) => {
    const response = await fetcher('/api/v1/auth/token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({ username: email, password, grant_type: 'password' }),
    });
    
    localStorage.setItem('token', response.access_token);
    const userData = await fetcher('/api/v1/auth/me');
    setUser(userData);
    return userData;
  };

  const signup = async (userData) => {
    const response = await fetcher('/api/v1/auth/signup', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
    
    localStorage.setItem('token', response.access_token);
    setUser(response.user);
    return response;
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
    router.push('/auth/signin');
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, signup, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);