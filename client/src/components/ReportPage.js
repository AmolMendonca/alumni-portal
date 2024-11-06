import React, { useState } from 'react';
import { AlertCircle, Send, X } from 'lucide-react';
import Navbar from './Navbar';
import Footer from './Footer';

const ReportPage = () => {
  const [formData, setFormData] = useState({
    email: '',
    title: '',
    description: '',
    type: 'bug' // or 'feature' or 'other'
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      // Add your API call here
      // For now, simulating an API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setSubmitStatus('success');
      setFormData({ email: '', title: '', description: '', type: 'bug' });
    } catch (error) {
      setSubmitStatus('error');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-white">
      <Navbar />
      
      <main className="max-w-2xl mx-auto px-4 pt-16 pb-20">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-4">
            Report an{' '}
            <span className="bg-purple-100 px-2 rounded-lg">Issue</span>
          </h1>
          <p className="text-gray-600">
            Help us improve by reporting bugs and sharing feedback
          </p>
        </div>

        {submitStatus === 'success' && (
          <div className="mb-8 p-4 bg-green-50 text-green-700 rounded-lg flex items-center justify-between">
            Thank you for your report! We'll look into it.
            <button 
              onClick={() => setSubmitStatus(null)}
              className="text-green-700 hover:text-green-800"
            >
              <X size={16} />
            </button>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Your Email
            </label>
            <input
              type="email"
              required
              placeholder="your@email.com"
              value={formData.email}
              onChange={(e) => setFormData({...formData, email: e.target.value})}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-300 focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Issue Type
            </label>
            <select
              value={formData.type}
              onChange={(e) => setFormData({...formData, type: e.target.value})}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-300 focus:border-transparent"
            >
              <option value="bug">Bug Report</option>
              <option value="feature">Feature Request</option>
              <option value="other">Other</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Title
            </label>
            <input
              type="text"
              required
              placeholder="Brief description of the issue"
              value={formData.title}
              onChange={(e) => setFormData({...formData, title: e.target.value})}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-300 focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Description
            </label>
            <textarea
              required
              placeholder="Please provide as much detail as possible..."
              rows={6}
              value={formData.description}
              onChange={(e) => setFormData({...formData, description: e.target.value})}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-300 focus:border-transparent"
            />
          </div>

          <button
            type="submit"
            disabled={isSubmitting}
            className={`w-full py-3 px-4 flex items-center justify-center gap-2 text-white rounded-lg transition-colors
              ${isSubmitting 
                ? 'bg-navy-800 cursor-not-allowed' 
                : 'bg-navy-900 hover:bg-navy-800'}`}
          >
            {isSubmitting ? (
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white" />
            ) : (
              <>
                <Send size={18} />
                Submit Report
              </>
            )}
          </button>

          <div className="mt-6 p-4 bg-blue-50 rounded-lg flex gap-3">
            <AlertCircle className="text-blue-600 flex-shrink-0" />
            <p className="text-sm text-blue-700">
              Before submitting a bug report, please ensure you've included:
              <ul className="list-disc ml-4 mt-2 space-y-1">
                <li>Steps to reproduce the issue</li>
                <li>Expected behavior</li>
                <li>Actual behavior</li>
                <li>Any error messages you received</li>
              </ul>
            </p>
          </div>
        </form>
      </main>

      <Footer />
    </div>
  );
};

export default ReportPage;