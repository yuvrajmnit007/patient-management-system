import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Check, X } from 'lucide-react';
import toast from 'react-hot-toast';
import { PageHeader } from '@/components/common/PageHeader';
import { DataTable } from '@/components/common/DataTable';
import { StatusBadge } from '@/components/common/StatusBadge';
import { ConfirmDialog } from '@/components/common/ConfirmDialog';
import { doctorService } from '@/services/doctorService';
import { Doctor } from '@/types/doctor';
import { getErrorMessage } from '@/api/error';

export const PendingDoctorsPage: React.FC = () => {
  const queryClient = useQueryClient();
  const [actionDoctor, setActionDoctor] = useState<{ id: number; action: 'approve' | 'reject' } | null>(null);

  const { data, isLoading, isError, refetch } = useQuery({
    queryKey: ['doctors', 'pending'],
    queryFn: () => doctorService.getPending(),
  });

  const approveMutation = useMutation({
    mutationFn: doctorService.approve,
    onSuccess: () => {
      toast.success('Doctor approved successfully');
      queryClient.invalidateQueries({ queryKey: ['doctors'] });
      setActionDoctor(null);
    },
    onError: (error) => toast.error(getErrorMessage(error)),
  });

  const rejectMutation = useMutation({
    mutationFn: doctorService.reject,
    onSuccess: () => {
      toast.success('Doctor rejected successfully');
      queryClient.invalidateQueries({ queryKey: ['doctors'] });
      setActionDoctor(null);
    },
    onError: (error) => toast.error(getErrorMessage(error)),
  });

  const columns = [
    { key: 'id', header: 'Doctor ID' },
    { key: 'full_name', header: 'Name' },
    { key: 'email', header: 'Email' },
    { key: 'phone_number', header: 'Phone' },
    { key: 'department', header: 'Department' },
    { key: 'specialization', header: 'Specialization' },
    { key: 'experience', header: 'Experience (Years)' },
    {
      key: 'status',
      header: 'Status',
      render: (item: Doctor) => <StatusBadge status={item.status} />,
    },
    {
      key: 'actions',
      header: 'Actions',
      render: (item: Doctor) => (
        <div className="flex items-center gap-2">
          <button onClick={() => setActionDoctor({ id: item.id, action: 'approve' })}
            className="flex items-center gap-1 px-3 py-1.5 bg-green-600 text-white rounded-lg text-xs font-medium hover:bg-green-700 transition-colors">
            <Check size={14} /> Approve
          </button>
          <button onClick={() => setActionDoctor({ id: item.id, action: 'reject' })}
            className="flex items-center gap-1 px-3 py-1.5 bg-red-600 text-white rounded-lg text-xs font-medium hover:bg-red-700 transition-colors">
            <X size={14} /> Reject
          </button>
        </div>
      ),
    },
  ];

  return (
    <div>
      <PageHeader title="Pending Doctors" description="Review and approve doctor registrations" />
      <DataTable columns={columns} data={data ?? []} isLoading={isLoading} isError={isError} onRetry={refetch}
        keyExtractor={(item) => item.id} emptyTitle="No pending doctors" emptyDescription="There are no doctors awaiting approval." />
      <ConfirmDialog isOpen={actionDoctor?.action === 'approve'} title="Approve Doctor"
        message="Are you sure you want to approve this doctor? They will be able to login and access the system."
        confirmText="Approve" confirmVariant="primary"
        onConfirm={() => actionDoctor && approveMutation.mutate(actionDoctor.id)} onCancel={() => setActionDoctor(null)} />
      <ConfirmDialog isOpen={actionDoctor?.action === 'reject'} title="Reject Doctor"
        message="Are you sure you want to reject this doctor? This action cannot be undone."
        confirmText="Reject" confirmVariant="danger"
        onConfirm={() => actionDoctor && rejectMutation.mutate(actionDoctor.id)} onCancel={() => setActionDoctor(null)} />
    </div>
  );
};
