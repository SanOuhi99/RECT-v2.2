import { useState } from 'react';
import { useSWRConfig } from 'swr';
import { CheckCircleIcon, ExclamationCircleIcon, ArrowPathIcon } from '@heroicons/react/24/outline'
import { useAuth } from '../../contexts/AuthContext';

export default function RunMatchingButton() {
  const [loading, setLoading] = useState(false);
  const [taskId, setTaskId] = useState(null);
  const [taskStatus, setTaskStatus] = useState(null);
  const { mutate } = useSWRConfig();
  const { user } = useAuth();

  const startMatching = async () => {
    setLoading(true);
    setTaskStatus(null);
    try {
      const response = await fetch('/api/v1/tasks/matching/start', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      const data = await response.json();
      setTaskId(data.task_id);
      pollTaskStatus(data.task_id);
    } catch (error) {
      setTaskStatus('error');
      setLoading(false);
    }
  };

  const pollTaskStatus = async (taskId) => {
    try {
      const response = await fetch(`/api/v1/tasks/matching/status/${taskId}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      const data = await response.json();
      
      if (data.status === 'SUCCESS') {
        setTaskStatus('success');
        setLoading(false);
        mutate('/api/v1/dashboard/stats');
        mutate('/api/v1/dashboard/matches');
      } else if (data.status === 'FAILURE') {
        setTaskStatus('failure');
        setLoading(false);
      } else {
        setTimeout(() => pollTaskStatus(taskId), 2000);
      }
    } catch (error) {
      setTaskStatus('error');
      setLoading(false);
    }
  };

  return (
    <div className="space-y-2">
      <button
        onClick={startMatching}
        disabled={loading || !user?.kvcore_token}
        className={`inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 ${loading ? 'opacity-75 cursor-not-allowed' : ''} ${!user?.kvcore_token ? 'bg-gray-400 hover:bg-gray-400 cursor-not-allowed' : ''}`}
      >
        {loading ? (
          <>
            <RefreshIcon className="animate-spin -ml-1 mr-2 h-5 w-5" />
            Processing...
          </>
        ) : (
          'Run Property Matching'
        )}
      </button>

      {!user?.kvcore_token && (
        <p className="text-sm text-gray-500">Please add your KvCore token in settings to enable matching</p>
      )}

      {taskStatus === 'success' && (
        <div className="flex items-center text-sm text-green-600">
          <CheckCircleIcon className="h-5 w-5 mr-1" />
          Matching completed successfully!
        </div>
      )}

      {taskStatus === 'failure' && (
        <div className="flex items-center text-sm text-red-600">
          <ExclamationCircleIcon className="h-5 w-5 mr-1" />
          Error occurred during matching
        </div>
      )}
    </div>
  );
}
