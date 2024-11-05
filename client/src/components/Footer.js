import React from 'react';
import { Users, HeartHandshake, Flag } from 'lucide-react';

const Footer = () => {
  const links = [
    { name: 'About Us', href: '/about', icon: Users },
    { name: 'Team', href: '/team', icon: HeartHandshake },
    { name: 'Report', href: '/report', icon: Flag }
  ];

  return (
    <footer className="fixed bottom-0 left-0 right-0 bg-white">
      <div className="max-w-4xl mx-auto px-4 py-4">
        <div className="flex flex-col sm:flex-row justify-center items-center space-y-2 sm:space-y-0 sm:space-x-8">
          {links.map((link) => {
            const IconComponent = link.icon;
            return (
              <a
                key={link.name}
                href={link.href}
                className="flex items-center text-gray-500 hover:text-navy-900 text-sm transition-colors"
              >
                <IconComponent size={14} className="mr-1.5" />
                <span>{link.name}</span>
              </a>
            );
          })}
        </div>
      </div>
    </footer>
  );
};

export default Footer;