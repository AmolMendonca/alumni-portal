import React, { useState } from 'react';
import { Search } from 'lucide-react';
import Navbar from './Navbar';
import SearchResults from './SearchResults';
import Footer from './Footer';
import axios from 'axios';


const LandingPage = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const categories = [
    { id: 1, name: 'Indian Internationals working in Tech' },
    { id: 2, name: 'Cathedral and John Connon Alumni' },
    { id: 3, name: 'Alumni who are a part of YC' }
  ];
  

  const API_URL = 'http://localhost:8000'; // Changed from 5000 to 8000

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
  
  return (
    <div className="min-h-screen bg-white">
      <Navbar />
      
      <main className="max-w-4xl mx-auto mt-32 px-4 pb-12">
        <h1 className="text-5xl font-bold text-center mb-16">
          Find your{' '}
          <span className="bg-purple-100 px-2 rounded-lg">hero.</span>
        </h1>

        <div className="relative max-w-3xl mx-auto mb-8">
          <form onSubmit={handleSearch}>
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Find me international students working at YC companies"
              className="w-full p-4 pr-12 text-gray-600 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-300 focus:border-transparent"
              disabled={isLoading}
            />
            <button 
              type="submit"
              className="absolute right-4 top-1/2 -translate-y-1/2 bg-navy-900 text-white p-2 rounded-md hover:bg-navy-800 disabled:opacity-50"
              disabled={isLoading}
            >
              <Search size={20} />
            </button>
          </form>
        </div>

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
            {searchQuery === '' && (
              <div className="flex flex-wrap justify-center gap-4">
                {categories.map((category) => (
                  <button
                    key={category.id}
                    className="px-4 py-2 bg-blue-50 text-blue-600 rounded-full hover:bg-blue-100 transition-colors"
                  >
                    {category.name} →
                  </button>
                ))}
              </div>
            )}
            <SearchResults results={searchResults} />
          </>
        )}
      </main>
      <Footer />
    </div>
  );
};

export default LandingPage;