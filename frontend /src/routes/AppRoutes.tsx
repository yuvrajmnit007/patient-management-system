import React from 'react';
import { Routes, Route, Navigate, Outlet } from 'react-router-dom';

import { useAuth } from '@/hooks/useAuth';
import { UserRole } from '@/types/auth';

import { Layout } from '@/components/layout/Layout';
import { LoginPage } from '@/pages/LoginPage';

import { AdminDashboard } from '@/pages/admin/AdminDashboard';
import { DoctorsPage } from '@/pages/admin/DoctorsPage';
import { PendingDoctorsPage } from '@/pages/admin/PendingDoctorsPage';
import { PatientsPage } from '@/pages/admin/PatientsPage';
import { AppointmentsPage } from '@/pages/admin/AppointmentsPage';
import { PrescriptionsPage } from '@/pages/admin/PrescriptionsPage';
import { AdminProfilePage } from '@/pages/admin/AdminProfilePage';

import { DoctorDashboard } from '@/pages/doctor/DoctorDashboard';
import { MyAppointmentsPage } from '@/pages/doctor/MyAppointmentsPage';
import { MyPrescriptionsPage } from '@/pages/doctor/MyPrescriptionsPage';
import { DoctorProfilePage } from '@/pages/doctor/DoctorProfilePage';


const FullPageSpinner = () => (
  <div className="min-h-screen flex items-center justify-center">
    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600" />
  </div>
);


const ProtectedRoute: React.FC = () => {
  const { isAuthenticated, isLoading } = useAuth();
  if (isLoading) return <FullPageSpinner />;
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  return <Outlet />;
};


const RoleProtectedRoute: React.FC<{ allowedRoles: UserRole[] }> = ({
  allowedRoles,
}) => {
  const { isAuthenticated, isLoading, user } = useAuth();

  if (isLoading) return <FullPageSpinner />;
  if (!isAuthenticated) return <Navigate to="/login" replace />;

  if (!user || !allowedRoles.includes(user.role)) {
    if (user?.role === 'admin') return <Navigate to="/admin/dashboard" replace />;
    if (user?.role === 'doctor') return <Navigate to="/doctor/dashboard" replace />;
    return <Navigate to="/login" replace />;
  }
  return <Outlet />;
};


export const AppRoutes: React.FC = () => {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />

      <Route element={<ProtectedRoute />}>
        <Route element={<Layout />}>

          {/* Admin section */}
          <Route element={<RoleProtectedRoute allowedRoles={['admin']} />}>
            <Route path="/admin" element={<Navigate to="/admin/dashboard" replace />} />
            <Route path="/admin/dashboard" element={<AdminDashboard />} />
            <Route path="/admin/doctors" element={<DoctorsPage />} />
            <Route path="/admin/pending-doctors" element={<PendingDoctorsPage />} />
            <Route path="/admin/patients" element={<PatientsPage />} />
            <Route path="/admin/appointments" element={<AppointmentsPage />} />
            <Route path="/admin/prescriptions" element={<PrescriptionsPage />} />
            <Route path="/admin/profile" element={<AdminProfilePage />} />
          </Route>

          {/* Doctor section */}
          <Route element={<RoleProtectedRoute allowedRoles={['doctor']} />}>
            <Route path="/doctor" element={<Navigate to="/doctor/dashboard" replace />} />
            <Route path="/doctor/dashboard" element={<DoctorDashboard />} />
            <Route path="/doctor/appointments" element={<MyAppointmentsPage />} />
            <Route path="/doctor/prescriptions" element={<MyPrescriptionsPage />} />
            <Route path="/doctor/profile" element={<DoctorProfilePage />} />
          </Route>

        </Route>
      </Route>

      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  );
};