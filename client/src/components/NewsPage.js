import React from 'react';
import { Calendar, ArrowUpRight, Share2 } from 'lucide-react';
import Navbar from './Navbar';
import Footer from './Footer';

const NewsPage = () => {
  const newsItems = [
    {
      id: 1, 
      title: "Sarah Chen (Class of '18) Launches AI Startup",
      category: "Startups",
      date: "Nov 2, 2024",
      preview: "Former Google engineer raises $5M seed round for new AI venture focusing on educational technology...",
      linkedInURL: "https://linkedin.com/in/sarahchen",
      image: "/api/placeholder/400/250"
    },
    {
      id: 2,
      title: "Alumni Mentor Program Reaches 100 Successful Matches", 
      category: "Community",
      date: "Nov 1, 2024",
      preview: "Our mentorship initiative continues to grow with alumni from top companies guiding the next generation...",
      linkedInURL: "https://linkedin.com/company/linkd",
      image: "/api/placeholder/400/250"
    },
    {
      id: 3,
      title: "Five Alumni Make Forbes 30 Under 30",
      category: "Achievements",
      date:  "Oct 30, 2024",
      preview: "Recent graduates recognized for innovations in fintech, healthcare, and sustainable energy...",
      linkedInURL: "https://forbes.com",
      image: "/api/placeholder/400/250"
    }
  ];

  const categories = [
    "All", "Startups", "Achievements", "Community", "Career Moves", "Events"  
  ];

  return (
    <div className="min-h-screen bg-white">
      <Navbar />
      
      <main className="max-w-4xl mx-auto px-4 pt-16 pb-20">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-4">
            Alumni{' '} 
            <span className="bg-purple-100 px-2 rounded-lg">News</span>
          </h1>
          <p className="text-gray-600">
            Stay updated with the latest from our community
          </p>
        </div>

        {/* Categories */}
        <div className="flex flex-wrap justify-center gap-3 mb-12">
          {categories.map((category) => (
            <button
              key={category}
              className={`px-4 py-2 rounded-full text-sm transition-colors ${
                category === 'All'
                  ? 'bg-navy-900 text-white'  
                  : 'bg-gray-50 text-gray-600 hover:bg-gray-100'
              }`}
            >
              {category}
            </button>
          ))}
        </div>

        {/* News Grid */} 
        <div className="space-y-8">
          {newsItems.map((item) => (
            <div
              key={item.id} 
              className="bg-white border border-gray-100 rounded-xl overflow-hidden hover:shadow-lg transition-shadow"
            >
              <div className="md:flex">
                <div className="md:w-1/3">
                  <img
                    src={item.image}
                    alt={item.title}
                    className="h-48 w-full object-cover"  
                  />
                </div>
                <div className="p-6 md:w-2/3">
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-sm text-blue-600 font-medium">
                      {item.category}
                    </span>
                    <div className="flex items-center space-x-2 text-gray-400">
                      <Calendar size={14} />
                      <span className="text-sm">{item.date}</span>
                    </div>
                  </div>
                  
                  <h2 className="text-xl font-semibold mb-3 hover:text-blue-600 transition-colors">
                    {item.title}
                  </h2>
                  
                  <p className="text-gray-600 mb-4">
                    {item.preview}
                  </p>
                  
                  <div className="flex items-center justify-between">
                    <a
                      href={item.linkedInURL}
                      target="_blank"
                      rel="noopener noreferrer"  
                      className="flex items-center text-blue-600 hover:text-blue-700 text-sm font-medium"
                    >
                      Read more
                      <ArrowUpRight size={16} className="ml-1" />  
                    </a>
                    
                    <div className="flex space-x-3">
                      <button className="text-gray-400 hover:text-gray-600 transition-colors">
                        <Share2 size={18} />
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Newsletter Signup */}
        <div className="mt-16 text-center bg-gray-50 rounded-xl p-8">
          <h2 className="text-2xl font-semibold mb-3">Stay in the Loop</h2>
          <p className="text-gray-600 mb-6 max-w-md mx-auto">
            Get weekly updates about alumni achievements, events, and opportunities.  
          </p>
          <div className="flex max-w-md mx-auto">
            <input 
              type="email"
              placeholder="Enter your email"
              className="flex-1 px-4 py-2 rounded-l-lg border border-r-0 border-gray-300 focus:outline-none focus:ring-2 focus:ring-purple-300"
            />
            <button className="px-6 py-2 bg-navy-900 text-white rounded-r-lg hover:bg-navy-800 transition-colors">
              Subscribe
            </button>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default NewsPage;