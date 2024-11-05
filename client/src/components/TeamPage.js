import React from 'react';
import Navbar from './Navbar';
import Footer from './Footer';
import { Github, Linkedin, Twitter } from 'lucide-react';

const TeamPage = () => {
  const teamMembers = [
    {
      name: 'Amol Mendonca',
      role: 'co-founder',
    //   image: '/api/placeholder/400/400',
      bio: 'building the future of alumni networking',
      social: {
        linkedin: 'https://linkedin.com/in/amol-mendonca',
        github: 'https://github.com/amolm',
        twitter: 'https://twitter.com/amolmendonca'
      }
    },
    {
      name: 'Satvik Kapoor',
      role: 'co-founder',
    //   image: '/api/placeholder/400/400',
      bio: 'connecting people with their heroes',
      social: {
        linkedin: 'https://linkedin.com/in/satvik-kapoor',
        github: 'https://github.com/satvikkapoor',
        twitter: 'https://twitter.com/satvikkapoor'
      }
    }
  ];

  return (
    <div className="min-h-screen bg-white">
      <Navbar />
      
      <main className="max-w-4xl mx-auto px-4 pt-16 pb-20">
        <div className="text-center mb-16">
          <h1 className="text-4xl font-bold mb-4">
            Meet the{' '}
            <span className="bg-purple-100 px-2 rounded-lg">founders</span>
          </h1>
          <p className="text-gray-600">
            Building the bridge between alumni and aspirations
          </p>
        </div>

        <div className="flex flex-wrap justify-center gap-12 md:gap-16">
          {teamMembers.map((member) => (
            <div 
              key={member.name} 
              className="flex flex-col items-center max-w-xs"
            >
              {/* <img
                src={member.image}
                alt={member.name}
                className="w-40 h-40 rounded-lg object-cover mb-4 bg-gray-100"
              /> */}
              <h3 className="text-xl font-semibold">{member.name}</h3>
              <p className="text-gray-500 mb-3">{member.role}</p>
              <p className="text-gray-600 text-center mb-4">{member.bio}</p>
              
              <div className="flex space-x-4">
                <a 
                  href={member.social.linkedin}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-gray-600 hover:text-blue-600 transition-colors"
                >
                  <Linkedin size={20} />
                </a>
                <a 
                  href={member.social.github}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-gray-600 hover:text-gray-900 transition-colors"
                >
                  <Github size={20} />
                </a>
                <a 
                  href={member.social.twitter}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-gray-600 hover:text-blue-400 transition-colors"
                >
                  <Twitter size={20} />
                </a>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-20 text-center">
          <div className="max-w-2xl mx-auto">
            <h2 className="text-2xl font-semibold mb-4">Our Mission</h2>
            <p className="text-gray-600">
              To empower students by connecting them with successful alumni, 
              creating pathways to opportunities and mentorship that shape 
              future careers.
            </p>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default TeamPage;