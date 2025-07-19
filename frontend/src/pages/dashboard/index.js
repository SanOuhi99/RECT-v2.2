import { useState } from 'react';
import Head from 'next/head';
import useSWR from 'swr';
import { useAuth } from '../../../contexts/AuthContext';
import Header from '../../../components/layout/Header';
import Footer from '../../../components/layout/Footer';
import StatsCard from '../../../components/dashboard/StatsCard';
import RecentMatches from '../../../components/dashboard/RecentMatches';
import RunMatchingButton from '../../../components/dashboard/RunMatchingButton';

export default function Dashboard() {
  const { user } = useAuth();
  const { data: stats, error: statsError } = useSWR('/api/v1/dashboard/stats');
  const { data: matches, error: matchesError } = useSWR('/api/v1/dashboard/matches');

  return (
    <div className="min-h-screen bg-gray-50">
      <Head>
        <title>Dashboard | Real Estate CRM</title>
      </Head>

      <Header />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        </div>

        <div className="grid grid-cols-1 gap-6 mb-8 sm:grid-cols-2 lg:grid-cols-3">
          <StatsCard 
            title="Total Matches" 
            value={stats?.total_matches || 0}
            icon={
              <svg className="h-6 w-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clipRule="evenodd" />
              </svg>
            }
          />
          <StatsCard 
            title="New This Week" 
            value={stats?.new_this_week || 0}
            icon={
              <svg className="h-6 w-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M12 1.586l-4 4v12.828l4-4V1.586zM3.707 3.293A1 1 0 002 4v10a1 1 0 00.293.707L6 18.414V5.586L3.707 3.293zM17.707 5.293L14 1.586v12.828l2.293 2.293A1 1 0 0018 16V6a1 1 0 00-.293-.707z" clipRule="evenodd" />
              </svg>
            }
          />
          <StatsCard 
            title="Success Rate" 
            value={`${stats?.success_rate ? (stats.success_rate * 100).toFixed(0) : 0}%`}
            icon={
              <svg className="h-6 w-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
            }
          />
        </div>

        <div className="mb-8">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-medium text-gray-900">Property Matching</h2>
            <RunMatchingButton />
          </div>
        </div>

        <div className="mb-8">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Recent Matches</h2>
          <RecentMatches matches={matches} />
        </div>
      </main>

      <Footer />
    </div>
  );
}