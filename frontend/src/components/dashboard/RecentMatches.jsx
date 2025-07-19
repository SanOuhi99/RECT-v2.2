import Link from 'next/link';

export default function RecentMatches({ matches }) {
  return (
    <div className="bg-white shadow overflow-hidden sm:rounded-lg">
      <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
        <h3 className="text-lg leading-6 font-medium text-gray-900">Recent Matches</h3>
      </div>
      <div className="bg-white overflow-hidden">
        <ul className="divide-y divide-gray-200">
          {matches?.length > 0 ? (
            matches.map((match) => (
              <li key={match.id}>
                <Link href={`/matches/${match.id}`}>
                  <a className="block hover:bg-gray-50">
                    <div className="px-4 py-4 sm:px-6">
                      <div className="flex items-center justify-between">
                        <p className="text-sm font-medium text-indigo-600 truncate">
                          {match.property_address}
                        </p>
                        <div className="ml-2 flex-shrink-0 flex">
                          <p className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                            New
                          </p>
                        </div>
                      </div>
                      <div className="mt-2 sm:flex sm:justify-between">
                        <div className="sm:flex">
                          <p className="flex items-center text-sm text-gray-500">
                            {match.contact_name}
                          </p>
                          <p className="mt-2 flex items-center text-sm text-gray-500 sm:mt-0 sm:ml-6">
                            {match.contact_email}
                          </p>
                        </div>
                        <div className="mt-2 flex items-center text-sm text-gray-500 sm:mt-0">
                          <p>
                            {new Date(match.match_date).toLocaleDateString()}
                          </p>
                        </div>
                      </div>
                    </div>
                  </a>
                </Link>
              </li>
            ))
          ) : (
            <li className="px-4 py-4 sm:px-6 text-center text-gray-500">
              No matches found
            </li>
          )}
        </ul>
      </div>
    </div>
  );
}