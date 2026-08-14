import React from 'react';
import { useAuth } from '@/hooks/useAuth';
import { PageHeader } from '@/components/common/PageHeader';
import { UserCircle, Mail, Shield } from 'lucide-react';

export const DoctorProfilePage: React.FC = () => {
  const { user } = useAuth();

  return (
    <div>
      <PageHeader title="My Profile" description="Your account information" />
      <div className="bg-white rounded-xl border border-gray-200 shadow-sm max-w-2xl">
        <div className="p-8 flex items-center gap-6 border-b border-gray-100">
          <div className="w-20 h-20 rounded-full bg-primary-100 flex items-center justify-center">
            <UserCircle size={40} className="text-primary-600" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-gray-900">{user?.full_name || user?.email}</h2>
            <p className="text-sm text-gray-500 capitalize">{user?.role?.toLowerCase()}</p>
          </div>
        </div>
        <div className="p-8 space-y-6">
          <div className="flex items-center gap-4">
            <div className="p-2 bg-gray-50 rounded-lg"><Mail size={18} className="text-gray-500" /></div>
            <div>
              <p className="text-sm font-medium text-gray-700">Email</p>
              <p className="text-sm text-gray-500">{user?.email}</p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <div className="p-2 bg-gray-50 rounded-lg"><Shield size={18} className="text-gray-500" /></div>
            <div>
              <p className="text-sm font-medium text-gray-700">Role</p>
              <p className="text-sm text-gray-500">{user?.role}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
