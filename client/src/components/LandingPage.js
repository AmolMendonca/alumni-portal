import React, { useState } from 'react';
import { Search, X } from 'lucide-react';
import Navbar from './Navbar';
import SearchResults from './SearchResults';
import Footer from './Footer';
import axios from 'axios';

const LandingPage = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const [showUniModal, setShowUniModal] = useState(false);
  const [selectedUni, setSelectedUni] = useState('');

  const universities = [
    'Harvard University',
    'Stanford University',
    'MIT',
    'Princeton University',
    'Yale University',
    'Columbia University',
    'UC Berkeley',
    'UPenn',
    'Northwestern University',
    'Duke University'
  ].sort();



  const categories = [
    { id: 1, name: 'Indian Internationals working in Tech' },
    { id: 2, name: 'Cathedral and John Connon Alumni' },
    { id: 3, name: 'Alumni who are a part of YC' }
  ];

  const API_URL = 'http://localhost:8000';

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;

    setIsLoading(true);
    setError(null);
    setSearchResults([]);

    try {
      const response = await fetch(`${API_URL}/search`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({ 
          query: searchQuery,
          k: 5 
        })
      });

      const data = await response.json();
      console.log('Search response:', data);

      if (data.status === 'success') {
        setSearchResults(data.results);
      } else {
        throw new Error(data.message || 'Search failed');
      }
    } catch (err) {
      console.error('Search error:', err);
      setError('Failed to search alumni. Please try again.');
      setSearchResults([]);
    } finally {
      setIsLoading(false);
    }
  };

  // New function to handle category click
  const handleCategoryClick = (categoryName) => {
    setSearchQuery(categoryName);
    // Focus the input field
    document.querySelector('input[type="text"]').focus();
  };

  const handleUniSubmit = (e) => {
    e.preventDefault();
    console.log('University requested:', selectedUni);
    // Here you would typically make an API call
    setShowUniModal(false);
    setSelectedUni('');
  };

  
  return (
    <div className="min-h-screen bg-white relative">
      <Navbar />
      
      <main className="max-w-4xl mx-auto mt-32 px-4 pb-12">
        <h1 className="text-5xl font-bold text-center mb-16">
            Direct access. {' '}
          <span className="bg-purple-100 px-2 rounded-lg">Real insights.</span>
        </h1>
  
        <div className="relative max-w-3xl mx-auto mb-8">
      <form onSubmit={handleSearch} className="relative">
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Find me international students working at YC companies"
          className="w-full p-4 pr-14 text-gray-600 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-300 focus:border-transparent"
          disabled={isLoading}
        />
        <button 
          type="submit"
          className="absolute right-2 top-1/2 -translate-y-1/2 w-10 h-10 bg-[#14142B] text-white rounded-lg hover:bg-opacity-90 disabled:opacity-50 flex items-center justify-center"
          disabled={isLoading}
        >
          <Search size={20} />
        </button>
      </form>
  
          {/* University indicator and request button */}
          <div className="flex items-center justify-center text-sm text-gray-500 mt-2">
            <span>Currently available for University of Michigan, Ann Arbor</span>
            <button 
              onClick={() => setShowUniModal(true)}
              className="ml-2 text-blue-600 hover:text-blue-700 transition-colors"
            >
              Requests →
            </button>
          </div>
        </div>
  
        {/* University Request Modal */}
        {showUniModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-lg p-6 max-w-md w-full relative">
              <div className="flex justify-between items-start mb-4">
                <h2 className="text-xl font-semibold">Request coverage at your university</h2>
                <button 
                  onClick={() => setShowUniModal(false)}
                  className="text-gray-500 hover:text-gray-700"
                >
                  <X size={20} />
                </button>
              </div>
              
              <form onSubmit={handleUniSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Select University
                  </label>
                  <select
                    value={selectedUni}
                    onChange={(e) => setSelectedUni(e.target.value)}
                    className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-300"
                    required
                  >
                    <option value="">Choose a university</option>
                    {universities.map((uni) => (
                      <option key={uni} value={uni}>{uni}</option>
                    ))}
                  </select>
                </div>
  
                <button
                  type="submit"
                  className="w-full py-2 bg-navy-900 text-white rounded-lg hover:bg-navy-800 transition-colors"
                >
                  Submit Request
                </button>
              </form>
            </div>
          </div>
        )}
  
        {error && (
          <div className="text-red-600 text-center mb-4 p-4 bg-red-50 rounded-lg">
            {error}
          </div>
        )}
  
        {isLoading ? (
          <div className="flex justify-center">
            <div className="animate-pulse text-gray-600">Searching...</div>
          </div>
        ) : (
          <>
            <div className="flex flex-wrap justify-center gap-4">
              {categories.map((category) => (
                <button
                  key={category.id}
                  onClick={() => handleCategoryClick(category.name)}
                  className="px-4 py-2 bg-blue-50 text-blue-600 rounded-full hover:bg-blue-100 transition-colors"
                >
                  {category.name} →
                </button>
              ))}
            </div>
            {searchResults.length > 0 && <SearchResults results={searchResults} />}
          </>
        )}
      </main>
      <Footer />
  
      {/* Click outside modal to close */}
      {showUniModal && (
        <div 
          className="fixed inset-0 z-40"
          onClick={() => setShowUniModal(false)}
        />
      )}
    </div>
  );
};

export default LandingPage;