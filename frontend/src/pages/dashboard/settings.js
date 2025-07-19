import { useState, useEffect } from 'react';
import { useAuth } from '../../../contexts/AuthContext';
import { fetcher } from '../../../lib/api';
import Header from '../../../components/layout/Header';
import Footer from '../../../components/layout/Footer';

export default function Settings() {
  const { user } = useAuth();
  const [kvcoreToken, setKvcoreToken] = useState('');
  const [notificationPrefs, setNotificationPrefs] = useState({
    email: true,
    frequency: 'weekly'
  });
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (user) {
      setKvcoreToken(user.kvcore_token || '');
      setNotificationPrefs(user.notification_preferences || {
        email: true,
        frequency: 'weekly'
      });
    }
  }, [user]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await fetcher('/api/v1/users/me', {
        method: 'PATCH',
        body: JSON.stringify({
          kvcore_token: kvcoreToken,
          notification_preferences: notificationPrefs
        })
      });
      setMessage('Settings saved successfully');
    } catch (error) {
      setMessage('Error saving settings');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-gray-900">Account Settings</h1>
        </div>

        <div className="bg-white shadow overflow-hidden sm:rounded-lg">
          <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
            <h3 className="text-lg leading-6 font-medium text-gray-900">Profile Information</h3>
          </div>
          <form onSubmit={handleSubmit}>
            <div className="px-4 py-5 sm:p-6 space-y-6">
              {message && (
                <div className={`p-4 rounded-md ${message.includes('success') ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'}`}>
                  {message}
                </div>
              )}

              <div className="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-6">
                <div className="sm:col-span-4">
                  <label htmlFor="kvcore-token" className="block text-sm font-medium text-gray-700">
                    KvCore API Token
                  </label>
                  <input
                    type="text"
                    name="kvcore-token"
                    id="kvcore-token"
                    value={kvcoreToken}
                    onChange={(e) => setKvcoreToken(e.target.value)}
                    className="mt-1 block w-full shadow-sm sm:text-sm focus:ring-indigo-500 focus:border-indigo-500 border-gray-300 rounded-md"
                  />
                </div>

                <div className="sm:col-span-4">
                  <label className="block text-sm font-medium text-gray-700">Notifications</label>
                  <div className="mt-2 space-y-4">
                    <div className="flex items-start">
                      <div className="flex items-center h-5">
                        <input
                          id="email-notifications"
                          name="email-notifications"
                          type="checkbox"
                          checked={notificationPrefs.email}
                          onChange={(e) => setNotificationPrefs({
                            ...notificationPrefs,
                            email: e.target.checked
                          })}
                          className="focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300 rounded"
                        />
                      </div>
                      <div className="ml-3 text-sm">
                        <label htmlFor="email-notifications" className="font-medium text-gray-700">
                          Email notifications
                        </label>
                      </div>
                    </div>

                    <div>
                      <label htmlFor="frequency" className="block text-sm font-medium text-gray-700">
                        Frequency
                      </label>
                      <select
                        id="frequency"
                        name="frequency"
                        value={notificationPrefs.frequency}
                        onChange={(e) => setNotificationPrefs({
                          ...notificationPrefs,
                          frequency: e.target.value
                        })}
                        className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
                      >
                        <option value="daily">Daily</option>
                        <option value="weekly">Weekly</option>
                        <option value="monthly">Monthly</option>
                      </select>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div className="px-4 py-3 bg-gray-50 text-right sm:px-6">
              <button
                type="submit"
                disabled={loading}
                className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? 'Saving...' : 'Save'}
              </button>
            </div>
          </form>
        </div>
      </main>

      <Footer />
    </div>
  );
}