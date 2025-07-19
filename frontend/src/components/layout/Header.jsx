import Link from 'next/link';
import { useAuth } from '../../contexts/AuthContext';

export default function Header() {
  const { user, logout } = useAuth();

  return (
    <header className="bg-white shadow">
      <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8 flex justify-between items-center">
        <div className="flex items-center space-x-4">
          <Link href="/">
            <a className="text-xl font-bold text-gray-900">RealEstateCRM</a>
          </Link>
          {user && (
            <nav className="hidden md:flex space-x-8">
              <Link href="/dashboard">
                <a className="text-gray-500 hover:text-gray-900">Dashboard</a>
              </Link>
            </nav>
          )}
        </div>
        
        {user ? (
          <div className="flex items-center space-x-4">
            <span className="text-sm text-gray-500">Hi, {user.full_name || user.email}</span>
            <button
              onClick={logout}
              className="text-sm text-gray-500 hover:text-gray-900"
            >
              Sign out
            </button>
          </div>
        ) : (
          <div className="flex items-center space-x-4">
            <Link href="/auth/signin">
              <a className="text-sm text-gray-500 hover:text-gray-900">Sign in</a>
            </Link>
            <Link href="/auth/signup">
              <a className="text-sm bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700">
                Sign up
              </a>
            </Link>
          </div>
        )}
      </div>
    </header>
  );
}