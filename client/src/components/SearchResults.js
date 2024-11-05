import React from 'react';
import { Briefcase, GraduationCap, School, ExternalLink } from 'lucide-react';

const SearchResults = ({ results }) => {
  if (!results || results.length === 0) {
    return null;
  }

  // Sort results by distance (similarity score) - lower distance means more relevant
  const sortedResults = [...results].sort((a, b) => a.Distance - b.Distance);

  return (
    <div className="mb-8">
      <div className="text-gray-600 mb-4">
        Found {results.length} alumni matching your search
      </div>
      <div className="space-y-4">
        {sortedResults.map((alumni) => (
          <div 
            key={alumni.AlumniID}
            className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm hover:shadow-md transition-shadow"
          >
            <div className="flex justify-between items-start">
              <div className="flex-1">
                <h3 className="text-xl font-semibold text-gray-900 flex items-center">
                  {alumni.FullName}
                </h3>
                <div className="mt-2 space-y-2">
                  <div className="flex items-center text-gray-600 gap-2">
                    <Briefcase size={18} className="flex-shrink-0" />
                    <span>{alumni.CurrentRole} at {alumni.Company}</span>
                  </div>
                  <div className="flex items-center text-gray-600 gap-2">
                    <GraduationCap size={18} className="flex-shrink-0" />
                    <span>{alumni.University}</span>
                  </div>
                  <div className="flex items-center text-gray-600 gap-2">
                    <School size={18} className="flex-shrink-0" />
                    <span>{alumni.HighSchool}</span>
                  </div>
                </div>
              </div>
              <a
                href={alumni.LinkedInURL}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center px-4 py-2 bg-blue-50 text-blue-600 rounded-full hover:bg-blue-100 transition-colors ml-4 flex-shrink-0"
              >
                <span className="mr-1">View Profile</span>
                <ExternalLink size={16} />
              </a>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SearchResults;