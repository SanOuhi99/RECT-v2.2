export default function Footer() {
  return (
    <footer className="bg-white border-t border-gray-200 mt-8">
      <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="flex items-center space-x-4">
            <span className="text-gray-500 text-sm">© {new Date().getFullYear()} Real Estate CRM Tracker</span>
          </div>
          <div className="mt-4 md:mt-0">
            <nav className="flex space-x-6">
              <a href="#" className="text-gray-500 hover:text-gray-900 text-sm">Privacy</a>
              <a href="#" className="text-gray-500 hover:text-gray-900 text-sm">Terms</a>
              <a href="#" className="text-gray-500 hover:text-gray-900 text-sm">Contact</a>
            </nav>
          </div>
        </div>
      </div>
    </footer>
  );
}