import React from 'react';
import { Briefcase, School, ExternalLink } from 'lucide-react';

const SearchResultCard = ({ alumni }) => {
  return (
    <div className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm hover:shadow-md transition-shadow">
      <div className="flex justify-between items-start">
        <div>
          <h3 className="text-xl font-semibold text-gray-900">{alumni.name}</h3>
          <div className="mt-2 space-y-2">
            <div className="flex items-center text-gray-600">
              <Briefcase size={18} className="mr-2" />
              <span>{alumni.role} at {alumni.company}</span>
            </div>
            <div className="flex items-center text-gray-600">
              <School size={18} className="mr-2" />
              <span>{alumni.highSchool}</span>
            </div>
          </div>
        </div>
        <a
          href={alumni.linkedinUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center px-4 py-2 bg-blue-50 text-blue-600 rounded-full hover:bg-blue-100 transition-colors"
        >
          <span className="mr-1">View Profile</span>
          <ExternalLink size={16} />
        </a>
      </div>
    </div>
  );
};

export default SearchResultCard;