import { getSession } from 'next-auth/react';
import api from '../../../lib/api';

export default async function handler(req, res) {
  const session = await getSession({ req });
  
  if (!session) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  try {
    const response = await api.get('/properties', {
      headers: { Authorization: `Bearer ${session.accessToken}` }
    });
    res.status(200).json(response.data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
}
