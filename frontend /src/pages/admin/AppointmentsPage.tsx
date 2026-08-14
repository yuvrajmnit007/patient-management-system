import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Plus, Pencil, Trash2, RotateCcw } from 'lucide-react';
import toast from 'react-hot-toast';
import { PageHeader } from '@/components/common/PageHeader';
import { DataTable } from '@/components/common/DataTable';
import { StatusBadge } from '@/components/common/StatusBadge';
import { ConfirmDialog } from '@/components/common/ConfirmDialog';
import { appointmentService } from '@/services/appointmentService';
import { Appointment } from '@/types/appointment';
import { getErrorMessage } from '@/api/error';

export const AppointmentsPage: React.FC = () => {
  const queryClient = useQueryClient();
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const [deleteId, setDeleteId] = useState<number | null>(null);
  const [restoreId, setRestoreId] = useState<number | null>(null);
  const limit = 10;

  const { data, isLoading, isError, refetch } = useQuery({
    queryKey: ['appointments', page, search],
    queryFn: () => appointmentService.getAll({ page, limit, search }),
  });

  const deleteMutation = useMutation({
    mutationFn: appointmentService.delete,
    onSuccess: () => {
      toast.success('Appointment deleted successfully');
      queryClient.invalidateQueries({ queryKey: ['appointments'] });
      setDeleteId(null);
    },
    onError: (error) => toast.error(getErrorMessage(error)),
  });

  const restoreMutation = useMutation({
    mutationFn: appointmentService.restore,
    onSuccess: () => {
      toast.success('Appointment restored successfully');
      queryClient.invalidateQueries({ queryKey: ['appointments'] });
      setRestoreId(null);
    },
    onError: (error) => toast.error(getErrorMessage(error)),
  });

  const columns = [
    { key: 'id', header: 'ID' },
    { key: 'patient', header: 'Patient', render: (item: Appointment) => item.patient?.full_name || '-' },
    { key: 'doctor', header: 'Doctor', render: (item: Appointment) => item.doctor?.full_name || '-' },
    { key: 'appointment_date', header: 'Date' },
    { key: 'appointment_time', header: 'Time' },
    { key: 'reason', header: 'Reason' },
    { key: 'status', header: 'Status', render: (item: Appointment) => <StatusBadge status={item.status} /> },
    {
      key: 'actions',
      header: 'Actions',
      render: (item: Appointment) => (
        <div className="flex items-center gap-2">
          <button className="p-1.5 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors">
            <Pencil size={16} />
          </button>
          {item.is_active ? (
            <button onClick={() => setDeleteId(item.id)} className="p-1.5 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors">
              <Trash2 size={16} />
            </button>
          ) : (
            <button onClick={() => setRestoreId(item.id)} className="p-1.5 text-gray-500 hover:text-green-600 hover:bg-green-50 rounded-lg transition-colors">
              <RotateCcw size={16} />
            </button>
          )}
        </div>
      ),
    },
  ];

  return (
    <div>
      <PageHeader title="Appointments" description="Manage all appointments" action={
        <button className="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg text-sm font-medium hover:bg-primary-700 transition-colors">
          <Plus size={18} /> Create Appointment
        </button>
      } />
      <DataTable columns={columns} data={data?.items ?? []} isLoading={isLoading} isError={isError} onRetry={refetch}
        searchPlaceholder="Search appointments..." onSearch={setSearch}
        pagination={{ page, limit, total: data?.total ?? 0, onPageChange: setPage }}
        keyExtractor={(item) => item.id} />
      <ConfirmDialog isOpen={!!deleteId} title="Delete Appointment" message="Are you sure you want to delete this appointment?"
        confirmText="Delete" confirmVariant="danger"
        onConfirm={() => deleteId && deleteMutation.mutate(deleteId)} onCancel={() => setDeleteId(null)} />
      <ConfirmDialog isOpen={!!restoreId} title="Restore Appointment" message="Are you sure you want to restore this appointment?"
        confirmText="Restore" confirmVariant="primary"
        onConfirm={() => restoreId && restoreMutation.mutate(restoreId)} onCancel={() => setRestoreId(null)} />
    </div>
  );
};
