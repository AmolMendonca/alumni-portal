import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';

const Navbar = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const isLandingPage = location.pathname === '/';

  return (
    <nav className="flex justify-between items-center p-6">
      <div>
        {!isLandingPage && (
          <button 
            onClick={() => navigate('/')}
            className="flex items-center text-gray-600 hover:text-gray-900 transition-colors"
          >
            <ArrowLeft size={20} className="mr-2" />
            <span>Back</span>
          </button>
        )}
      </div>
      <div className="flex items-center space-x-6">
        <button className="px-4 py-2 bg-navy-900 text-white rounded-md hover:bg-navy-800">
          Sign Up
        </button>
      </div>
    </nav>
  );
};

export default Navbar;