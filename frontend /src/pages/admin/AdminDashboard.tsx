import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { Users, Stethoscope, UserCheck, CalendarDays } from 'lucide-react';

import { PageHeader } from '@/components/common/PageHeader';
import { ErrorState } from '@/components/common/ErrorState';
import { patientService } from '@/services/patientService';
import { doctorService } from '@/services/doctorService';
import { appointmentService } from '@/services/appointmentService';

const StatCard: React.FC<{
  title: string;
  value: number | string;
  loading?: boolean;
  icon: React.ReactNode;
  color: string;
}> = ({ title, value, loading, icon, color }) => (
  <div className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
    <div className="flex items-center justify-between">
      <div>
        <p className="text-sm font-medium text-gray-500">{title}</p>
        <p className="text-2xl font-bold text-gray-900 mt-1">
          {loading ? '…' : value}
        </p>
      </div>
      <div className={`p-3 rounded-lg ${color}`}>{icon}</div>
    </div>
  </div>
);

export const AdminDashboard: React.FC = () => {
  const today = new Date().toISOString().split('T')[0];

  const patients = useQuery({
    queryKey: ['patients', 'count'],
    queryFn: () => patientService.getAll({ limit: 1 }),
  });
  const doctors = useQuery({
    queryKey: ['doctors', 'count'],
    queryFn: () => doctorService.getAll({ limit: 1 }),
  });
  const pending = useQuery({
    queryKey: ['doctors', 'pending'],
    queryFn: () => doctorService.getPending(),
  });
  const appointmentsToday = useQuery({
    queryKey: ['appointments', 'today', today],
    queryFn: () =>
      appointmentService.getAll({ limit: 1, appointment_date: today }),
  });

  const anyError =
    patients.isError ||
    doctors.isError ||
    pending.isError ||
    appointmentsToday.isError;

  if (anyError) {
    return <ErrorState onRetry={() => window.location.reload()} />;
  }

  return (
    <div>
      <PageHeader title="Dashboard" description="Overview of hospital operations" />
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Total Patients"
          value={patients.data?.total ?? 0}
          loading={patients.isLoading}
          icon={<Users size={20} className="text-blue-600" />}
          color="bg-blue-50"
        />
        <StatCard
          title="Total Doctors"
          value={doctors.data?.total ?? 0}
          loading={doctors.isLoading}
          icon={<Stethoscope size={20} className="text-primary-600" />}
          color="bg-primary-50"
        />
        <StatCard
          title="Pending Doctors"
          value={pending.data?.length ?? 0}
          loading={pending.isLoading}
          icon={<UserCheck size={20} className="text-yellow-600" />}
          color="bg-yellow-50"
        />
        <StatCard
          title="Today's Appointments"
          value={appointmentsToday.data?.total ?? 0}
          loading={appointmentsToday.isLoading}
          icon={<CalendarDays size={20} className="text-purple-600" />}
          color="bg-purple-50"
        />
      </div>
    </div>
  );
};