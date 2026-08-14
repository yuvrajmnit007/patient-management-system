import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Check, FilePlus } from 'lucide-react';
import toast from 'react-hot-toast';
import { useAuth } from '@/hooks/useAuth';
import { PageHeader } from '@/components/common/PageHeader';
import { DataTable } from '@/components/common/DataTable';
import { StatusBadge } from '@/components/common/StatusBadge';
import { ConfirmDialog } from '@/components/common/ConfirmDialog';
import { appointmentService } from '@/services/appointmentService';
import { Appointment } from '@/types/appointment';
import { getErrorMessage } from '@/api/error';

export const MyAppointmentsPage: React.FC = () => {
  const { user } = useAuth();
  const queryClient = useQueryClient();
  const [page, setPage] = useState(1);
  const [confirmId, setConfirmId] = useState<number | null>(null);
  const limit = 10;

  const { data, isLoading, isError, refetch } = useQuery({
    queryKey: ['appointments', 'my', page],
    queryFn: () => appointmentService.getAll({ doctor_id: user?.id, page, limit }),
    enabled: !!user?.id,
  });

  const confirmMutation = useMutation({
    mutationFn: appointmentService.confirm,
    onSuccess: () => {
      toast.success('Appointment confirmed');
      queryClient.invalidateQueries({ queryKey: ['appointments'] });
      setConfirmId(null);
    },
    onError: (error) => toast.error(getErrorMessage(error)),
  });

  const columns = [
    { key: 'id', header: 'ID' },
    { key: 'patient', header: 'Patient', render: (item: Appointment) => item.patient?.full_name || '-' },
    { key: 'appointment_date', header: 'Date' },
    { key: 'appointment_time', header: 'Time' },
    { key: 'reason', header: 'Reason' },
    { key: 'status', header: 'Status', render: (item: Appointment) => <StatusBadge status={item.status} /> },
    {
      key: 'actions',
      header: 'Actions',
      render: (item: Appointment) => (
        <div className="flex items-center gap-2">
          {item.status === 'Pending' && (
            <button onClick={() => setConfirmId(item.id)}
              className="flex items-center gap-1 px-3 py-1.5 bg-blue-600 text-white rounded-lg text-xs font-medium hover:bg-blue-700 transition-colors">
              <Check size={14} /> Confirm
            </button>
          )}
          {item.status === 'Confirmed' && (
            <button
              className="flex items-center gap-1 px-3 py-1.5 bg-primary-600 text-white rounded-lg text-xs font-medium hover:bg-primary-700 transition-colors">
              <FilePlus size={14} /> Prescribe
            </button>
          )}
        </div>
      ),
    },
  ];

  return (
    <div>
      <PageHeader title="My Appointments" description="Appointments assigned to you" />
      <DataTable columns={columns} data={data?.items ?? []} isLoading={isLoading} isError={isError} onRetry={refetch}
        pagination={{ page, limit, total: data?.total ?? 0, onPageChange: setPage }}
        keyExtractor={(item) => item.id} />
      <ConfirmDialog isOpen={!!confirmId} title="Confirm Appointment" message="Are you sure you want to confirm this appointment?"
        confirmText="Confirm" confirmVariant="primary"
        onConfirm={() => confirmId && confirmMutation.mutate(confirmId)} onCancel={() => setConfirmId(null)} />
    </div>
  );
};
