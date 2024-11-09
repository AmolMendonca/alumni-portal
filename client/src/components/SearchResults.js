import React, { useState } from 'react';
import { Briefcase, GraduationCap, School, ExternalLink, RefreshCw } from 'lucide-react';

const AlumniCard = ({ alumni }) => (
  <div className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm hover:shadow-md transition-shadow">
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
);

const SearchResults = ({ results, onSearchAgain }) => {
  const [showAllResults, setShowAllResults] = useState(false);

  if (!results || results.length === 0) {
    return null;
  }

  // Sort results by distance (similarity score)
  const sortedResults = [...results].sort((a, b) => a.Distance - b.Distance);
  
  // Check if the top result has a high similarity score
  const hasHighSimilarity = sortedResults[0]?.Distance >= 0.991;
  
  // Determine which results to display
  let displayResults = sortedResults;
  if (hasHighSimilarity && !showAllResults) {
    displayResults = [sortedResults[0]];
  } else {
    displayResults = sortedResults.slice(0, 5);
  }

  return (
    <div className="mt-12 mb-8">
      <div className="flex items-center gap-2 mb-4">
        <div className="text-gray-600">
          {hasHighSimilarity && !showAllResults ? (
            <div className="flex items-center">
              <div className="px-3 py-1 bg-green-50 text-green-700 rounded-full text-sm font-medium">
                Perfect Match Found
              </div>
              <div className="mx-2 text-gray-400">•</div>
              <div className="text-gray-600">
                {results.length - 1} additional {results.length - 1 === 1 ? 'result' : 'results'} available
              </div>
            </div>
          ) : (
            `Found ${results.length} alumni matching your search`
          )}
        </div>
      </div>
      
      <div className="space-y-4">
        {displayResults.map((alumni) => (
          <AlumniCard key={alumni.AlumniID} alumni={alumni} />
        ))}
      </div>

      {hasHighSimilarity && !showAllResults && results.length > 1 && (
        <button
          onClick={() => setShowAllResults(true)}
          className="mt-4 flex items-center gap-2 px-4 py-2 text-blue-600 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors"
        >
          <RefreshCw size={18} />
          Show more results
        </button>
      )}
      
      {showAllResults && (
        <button
          onClick={() => {
            setShowAllResults(false);
            if (onSearchAgain) onSearchAgain();
          }}
          className="mt-4 flex items-center gap-2 px-4 py-2 text-blue-600 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors"
        >
          <RefreshCw size={18} />
          Search again
        </button>
      )}
    </div>
  );
};

export default SearchResults;