import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { CalendarDays, FileText, CheckCircle, Clock } from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';
import { PageHeader } from '@/components/common/PageHeader';
import { LoadingSpinner } from '@/components/common/LoadingSpinner';
import { ErrorState } from '@/components/common/ErrorState';
import { appointmentService } from '@/services/appointmentService';
import { prescriptionService } from '@/services/prescriptionService';

const StatCard: React.FC<{
  title: string;
  value: number | string;
  icon: React.ReactNode;
  color: string;
}> = ({ title, value, icon, color }) => (
  <div className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
    <div className="flex items-center justify-between">
      <div>
        <p className="text-sm font-medium text-gray-500">{title}</p>
        <p className="text-2xl font-bold text-gray-900 mt-1">{value}</p>
      </div>
      <div className={`p-3 rounded-lg ${color}`}>{icon}</div>
    </div>
  </div>
);

export const DoctorDashboard: React.FC = () => {
  const { user } = useAuth();

  const { data: appointments, isLoading: aLoading, isError: aError } = useQuery({
    queryKey: ['appointments', 'doctor', user?.id],
    queryFn: () => appointmentService.getAll({ doctor_id: user?.id, limit: 100 }),
    enabled: !!user?.id,
  });

  const { data: prescriptions, isLoading: pLoading, isError: pError } = useQuery({
    queryKey: ['prescriptions', 'doctor', user?.id],
    queryFn: () => prescriptionService.getAll({ doctor_id: user?.id, limit: 100 }),
    enabled: !!user?.id,
  });

  const isLoading = aLoading || pLoading;
  const isError = aError || pError;

  if (isLoading) return <LoadingSpinner />;
  if (isError) return <ErrorState onRetry={() => window.location.reload()} />;

  const today = new Date().toISOString().split('T')[0];
  const todayAppointments = appointments?.items.filter((a) => a.appointment_date === today).length ?? 0;
  const confirmedAppointments = appointments?.items.filter((a) => a.status === 'Confirmed').length ?? 0;
  const completedAppointments = appointments?.items.filter((a) => a.status === 'Completed').length ?? 0;
  const totalPrescriptions = prescriptions?.total ?? 0;

  return (
    <div>
      <PageHeader title="Dashboard" description="Overview of your practice" />
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard title="Today's Appointments" value={todayAppointments}
          icon={<CalendarDays size={20} className="text-primary-600" />} color="bg-primary-50" />
        <StatCard title="Confirmed" value={confirmedAppointments}
          icon={<CheckCircle size={20} className="text-blue-600" />} color="bg-blue-50" />
        <StatCard title="Completed" value={completedAppointments}
          icon={<Clock size={20} className="text-green-600" />} color="bg-green-50" />
        <StatCard title="My Prescriptions" value={totalPrescriptions}
          icon={<FileText size={20} className="text-purple-600" />} color="bg-purple-50" />
      </div>
    </div>
  );
};
