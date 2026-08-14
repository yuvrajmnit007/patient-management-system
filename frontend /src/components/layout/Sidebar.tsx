import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  LayoutDashboard,
  Users,
  UserCheck,
  UserPlus,
  CalendarDays,
  FileText,
  UserCircle,
  LogOut,
  Menu,
  X,
  Stethoscope,
} from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';

interface NavItem {
  label: string;
  path: string;
  icon: React.ReactNode;
  roles: ('ADMIN' | 'DOCTOR')[];
}

const navItems: NavItem[] = [
  {
    label: 'Dashboard',
    path: '/admin/dashboard',
    icon: <LayoutDashboard size={20} />,
    roles: ['ADMIN'],
  },
  {
    label: 'Doctors',
    path: '/admin/doctors',
    icon: <Stethoscope size={20} />,
    roles: ['ADMIN'],
  },
  {
    label: 'Pending Doctors',
    path: '/admin/pending-doctors',
    icon: <UserCheck size={20} />,
    roles: ['ADMIN'],
  },
  {
    label: 'Patients',
    path: '/admin/patients',
    icon: <Users size={20} />,
    roles: ['ADMIN'],
  },
  {
    label: 'Appointments',
    path: '/admin/appointments',
    icon: <CalendarDays size={20} />,
    roles: ['ADMIN'],
  },
  {
    label: 'Prescriptions',
    path: '/admin/prescriptions',
    icon: <FileText size={20} />,
    roles: ['ADMIN'],
  },
  {
    label: 'Profile',
    path: '/admin/profile',
    icon: <UserCircle size={20} />,
    roles: ['ADMIN'],
  },
  {
    label: 'Dashboard',
    path: '/doctor/dashboard',
    icon: <LayoutDashboard size={20} />,
    roles: ['DOCTOR'],
  },
  {
    label: 'My Appointments',
    path: '/doctor/appointments',
    icon: <CalendarDays size={20} />,
    roles: ['DOCTOR'],
  },
  {
    label: 'My Prescriptions',
    path: '/doctor/prescriptions',
    icon: <FileText size={20} />,
    roles: ['DOCTOR'],
  },
  {
    label: 'Profile',
    path: '/doctor/profile',
    icon: <UserCircle size={20} />,
    roles: ['DOCTOR'],
  },
];

export const Sidebar: React.FC = () => {
  const { user, logout, hasRole } = useAuth();
  const location = useLocation();
  const [mobileOpen, setMobileOpen] = useState(false);

  const filteredNavItems = navItems.filter((item) =>
    item.roles.some((role) => hasRole(role))
  );

  const isActive = (path: string) => location.pathname === path;

  return (
    <>
      {/* Mobile menu button */}
      <button
        onClick={() => setMobileOpen(!mobileOpen)}
        className="lg:hidden fixed top-4 left-4 z-50 p-2 bg-white rounded-lg shadow-sm border border-gray-200"
      >
        {mobileOpen ? <X size={20} /> : <Menu size={20} />}
      </button>

      {/* Mobile overlay */}
      {mobileOpen && (
        <div
          className="lg:hidden fixed inset-0 bg-black/50 z-30"
          onClick={() => setMobileOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`fixed lg:sticky top-0 left-0 z-40 h-screen w-64 bg-white border-r border-gray-200 flex flex-col transition-transform duration-300 lg:translate-x-0 ${
          mobileOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="p-6 border-b border-gray-100">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-primary-600 flex items-center justify-center">
              <Stethoscope size={18} className="text-white" />
            </div>
            <div>
              <h1 className="font-bold text-lg text-gray-900 leading-tight">HMS</h1>
              <p className="text-xs text-gray-500">Hospital Management</p>
            </div>
          </div>
        </div>

        <nav className="flex-1 overflow-y-auto py-4 px-3">
          <ul className="space-y-1">
            {filteredNavItems.map((item) => (
              <li key={item.path}>
                <Link
                  to={item.path}
                  onClick={() => setMobileOpen(false)}
                  className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                    isActive(item.path)
                      ? 'bg-primary-50 text-primary-700'
                      : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                  }`}
                >
                  <span className={isActive(item.path) ? 'text-primary-600' : 'text-gray-400'}>
                    {item.icon}
                  </span>
                  {item.label}
                </Link>
              </li>
            ))}
          </ul>
        </nav>

        <div className="p-4 border-t border-gray-200">
          <div className="flex items-center gap-3 px-3 py-2 mb-3">
            <div className="w-8 h-8 rounded-full bg-primary-100 flex items-center justify-center">
              <UserCircle size={18} className="text-primary-600" />
            </div>
            <div className="min-w-0">
              <p className="text-sm font-medium text-gray-900 truncate">{user?.full_name || user?.email}</p>
              <p className="text-xs text-gray-500 capitalize">{user?.role?.toLowerCase()}</p>
            </div>
          </div>
          <button
            onClick={logout}
            className="flex items-center gap-3 w-full px-3 py-2.5 rounded-lg text-sm font-medium text-red-600 hover:bg-red-50 transition-colors"
          >
            <LogOut size={18} />
            Logout
          </button>
        </div>
      </aside>
    </>
  );
};
