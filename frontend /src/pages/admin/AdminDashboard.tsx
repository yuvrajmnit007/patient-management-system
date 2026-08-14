import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { Users, Stethoscope, UserCheck, CalendarDays } from 'lucide-react';
import { PageHeader } from '@/components/common/PageHeader';
import { LoadingSpinner } from '@/components/common/LoadingSpinner';
import { ErrorState } from '@/components/common/ErrorState';
import { patientService } from '@/services/patientService';
import { doctorService } from '@/services/doctorService';
import { appointmentService } from '@/services/appointmentService';

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

export const AdminDashboard: React.FC = () => {
  const { data: patients, isLoading: pLoading, isError: pError } = useQuery({
    queryKey: ['patients', 'count'],
    queryFn: () => patientService.getAll({ limit: 1 }),
  });

  const { data: doctors, isLoading: dLoading, isError: dError } = useQuery({
    queryKey: ['doctors', 'count'],
    queryFn: () => doctorService.getAll({ limit: 1 }),
  });

  const { data: pendingDoctors, isLoading: pdLoading } = useQuery({
    queryKey: ['doctors', 'pending'],
    queryFn: () => doctorService.getPending(),
  });

  const { data: appointments, isLoading: aLoading, isError: aError } = useQuery({
    queryKey: ['appointments', 'today'],
    queryFn: () => appointmentService.getAll({ limit: 100 }),
  });

  const isLoading = pLoading || dLoading || pdLoading || aLoading;
  const isError = pError || dError || aError;

  if (isLoading) return <LoadingSpinner />;
  if (isError) return <ErrorState onRetry={() => window.location.reload()} />;

  const today = new Date().toISOString().split('T')[0];
  const todayAppointments = appointments?.items.filter(
    (a) => a.appointment_date === today
  ).length ?? 0;

  return (
    <div>
      <PageHeader title="Dashboard" description="Overview of hospital operations" />
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Total Patients"
          value={patients?.total ?? 0}
          icon={<Users size={20} className="text-blue-600" />}
          color="bg-blue-50"
        />
        <StatCard
          title="Total Doctors"
          value={doctors?.total ?? 0}
          icon={<Stethoscope size={20} className="text-primary-600" />}
          color="bg-primary-50"
        />
        <StatCard
          title="Pending Doctors"
          value={pendingDoctors?.length ?? 0}
          icon={<UserCheck size={20} className="text-yellow-600" />}
          color="bg-yellow-50"
        />
        <StatCard
          title="Today's Appointments"
          value={todayAppointments}
          icon={<CalendarDays size={20} className="text-purple-600" />}
          color="bg-purple-50"
        />
      </div>
    </div>
  );
};
