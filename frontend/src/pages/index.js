import Head from 'next/head';
import Link from 'next/link';
import { useAuth } from '../contexts/AuthContext';

export default function Home() {
  const { user } = useAuth();

  return (
    <div className="min-h-screen bg-gray-50">
      <Head>
        <title>Real Estate CRM Tracker</title>
        <meta name="description" content="Automated property matching for real estate professionals" />
      </Head>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center">
          <h1 className="text-4xl font-extrabold text-gray-900 sm:text-5xl sm:tracking-tight lg:text-6xl">
            Automate Your Property Matching
          </h1>
          <p className="mt-6 max-w-lg mx-auto text-xl text-gray-500">
            Connect your CRM and get automatic property matches for your clients
          </p>
          <div className="mt-10 flex justify-center space-x-4">
            {user ? (
              <Link href="/dashboard">
                <a className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700">
                  Go to Dashboard
                </a>
              </Link>
            ) : (
              <>
                <Link href="/auth/signup">
                  <a className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700">
                    Get Started
                  </a>
                </Link>
                <Link href="/auth/signin">
                  <a className="inline-flex items-center px-6 py-3 border border-gray-300 text-base font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
                    Sign In
                  </a>
                </Link>
              </>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}