import { createContext, useContext, useState, useEffect } from 'react';
import api from '../lib/api';

const PropertyContext = createContext();

export function PropertyProvider({ children }) {
  const [properties, setProperties] = useState([]);
  const [loading, setLoading] = useState(true);

  const refreshProperties = async () => {
    try {
      const { data } = await api.get('/properties');
      setProperties(data);
    } catch (error) {
      console.error('Error fetching properties:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    refreshProperties();
  }, []);

  return (
    <PropertyContext.Provider value={{ properties, loading, refreshProperties }}>
      {children}
    </PropertyContext.Provider>
  );
}

export const useProperties = () => useContext(PropertyContext);
