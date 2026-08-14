import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { CalendarDays, FileText, CheckCircle, Clock } from 'lucide-react';

import { PageHeader } from '@/components/common/PageHeader';
import { LoadingSpinner } from '@/components/common/LoadingSpinner';
import { ErrorState } from '@/components/common/ErrorState';
import { useCurrentDoctor } from '@/hooks/useCurrentDoctor';
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
  const doctorQ = useCurrentDoctor();
  const doctorId = doctorQ.data?.doctor_id;
  const today = new Date().toISOString().split('T')[0];

  const appointmentsToday = useQuery({
    queryKey: ['appointments', 'doctor', doctorId, 'today', today],
    queryFn: () =>
      appointmentService.getAll({
        doctor_id: doctorId,
        appointment_date: today,
        limit: 1,
      }),
    enabled: !!doctorId,
  });

  const confirmedQ = useQuery({
    queryKey: ['appointments', 'doctor', doctorId, 'confirmed'],
    queryFn: () =>
      appointmentService.getAll({
        doctor_id: doctorId,
        appointment_status: 'Confirmed',
        limit: 1,
      }),
    enabled: !!doctorId,
  });

  const completedQ = useQuery({
    queryKey: ['appointments', 'doctor', doctorId, 'completed'],
    queryFn: () =>
      appointmentService.getAll({
        doctor_id: doctorId,
        appointment_status: 'Completed',
        limit: 1,
      }),
    enabled: !!doctorId,
  });

  const prescriptionsQ = useQuery({
    queryKey: ['prescriptions', 'doctor', doctorId],
    queryFn: () => prescriptionService.getAll({ doctor_id: doctorId, limit: 1 }),
    enabled: !!doctorId,
  });

  if (doctorQ.isLoading) return <LoadingSpinner />;
  if (doctorQ.isError) return <ErrorState onRetry={() => doctorQ.refetch()} />;

  return (
    <div>
      <PageHeader title="Dashboard" description="Overview of your practice" />
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Today's Appointments"
          value={appointmentsToday.data?.total ?? 0}
          icon={<CalendarDays size={20} className="text-primary-600" />}
          color="bg-primary-50"
        />
        <StatCard
          title="Confirmed"
          value={confirmedQ.data?.total ?? 0}
          icon={<CheckCircle size={20} className="text-blue-600" />}
          color="bg-blue-50"
        />
        <StatCard
          title="Completed"
          value={completedQ.data?.total ?? 0}
          icon={<Clock size={20} className="text-green-600" />}
          color="bg-green-50"
        />
        <StatCard
          title="My Prescriptions"
          value={prescriptionsQ.data?.total ?? 0}
          icon={<FileText size={20} className="text-purple-600" />}
          color="bg-purple-50"
        />
      </div>
    </div>
  );
};