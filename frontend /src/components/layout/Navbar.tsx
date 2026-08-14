import React from 'react';
import { useAuth } from '@/hooks/useAuth';
import { Bell, UserCircle } from 'lucide-react';

export const Navbar: React.FC = () => {
  const { user } = useAuth();

  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-20">
      <div className="flex items-center justify-between h-16 px-4 sm:px-6 lg:px-8">
        <div className="lg:hidden w-8" /> {/* Spacer for mobile menu button */}
        <div />
        <div className="flex items-center gap-4">
          <button className="relative p-2 text-gray-400 hover:text-gray-600 transition-colors rounded-lg hover:bg-gray-50">
            <Bell size={20} />
            <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-red-500 rounded-full" />
          </button>
          <div className="flex items-center gap-3">
            <div className="hidden sm:block text-right">
              <p className="text-sm font-medium text-gray-900">{user?.full_name || user?.email}</p>
              <p className="text-xs text-gray-500 capitalize">{user?.role?.toLowerCase()}</p>
            </div>
            <div className="w-9 h-9 rounded-full bg-primary-100 flex items-center justify-center">
              <UserCircle size={20} className="text-primary-600" />
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};
