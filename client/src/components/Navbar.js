import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav className="flex justify-between items-center p-6">
      <Link to="/" className="text-xl font-bold">
        Linkd
      </Link>
      <div className="flex items-center space-x-6">
        <Link 
          to="/news" 
          className="text-gray-600 hover:text-gray-900 transition-colors"
        >
          News
        </Link>
        <Link 
          to="/team" 
          className="text-gray-600 hover:text-gray-900 transition-colors"
        >
          Team
        </Link>
        <button className="px-4 py-2 bg-navy-900 text-white rounded-md hover:bg-navy-800">
          Sign Up
        </button>
      </div>
    </nav>
  );
};

export default Navbar;