import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from '@/hooks/useAuth';
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

interface ProtectedRouteProps {
  children: React.ReactNode;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600" />
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
};

interface RoleProtectedRouteProps extends ProtectedRouteProps {
  allowedRoles: ('ADMIN' | 'DOCTOR')[];
}

const RoleProtectedRoute: React.FC<RoleProtectedRouteProps> = ({
  children,
  allowedRoles,
}) => {
  const { isAuthenticated, isLoading, user } = useAuth();

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600" />
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (!allowedRoles.includes(user!.role)) {
    // Redirect to appropriate dashboard based on role
    if (user!.role === 'ADMIN') {
      return <Navigate to="/admin/dashboard" replace />;
    }
    if (user!.role === 'DOCTOR') {
      return <Navigate to="/doctor/dashboard" replace />;
    }
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
};

export const AppRoutes: React.FC = () => {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route
        element={
          <ProtectedRoute>
            <Layout />
          </ProtectedRoute>
        }
      >
        {/* Admin Routes */}
        <Route
          path="/admin/*"
          element={
            <RoleProtectedRoute allowedRoles={['ADMIN']}>
              <Routes>
                <Route path="dashboard" element={<AdminDashboard />} />
                <Route path="doctors" element={<DoctorsPage />} />
                <Route path="pending-doctors" element={<PendingDoctorsPage />} />
                <Route path="patients" element={<PatientsPage />} />
                <Route path="appointments" element={<AppointmentsPage />} />
                <Route path="prescriptions" element={<PrescriptionsPage />} />
                <Route path="profile" element={<AdminProfilePage />} />
                <Route path="*" element={<Navigate to="/admin/dashboard" replace />} />
              </Routes>
            </RoleProtectedRoute>
          }
        />
        {/* Doctor Routes */}
        <Route
          path="/doctor/*"
          element={
            <RoleProtectedRoute allowedRoles={['DOCTOR']}>
              <Routes>
                <Route path="dashboard" element={<DoctorDashboard />} />
                <Route path="appointments" element={<MyAppointmentsPage />} />
                <Route path="prescriptions" element={<MyPrescriptionsPage />} />
                <Route path="profile" element={<DoctorProfilePage />} />
                <Route path="*" element={<Navigate to="/doctor/dashboard" replace />} />
              </Routes>
            </RoleProtectedRoute>
          }
        />
      </Route>
      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  );
};
