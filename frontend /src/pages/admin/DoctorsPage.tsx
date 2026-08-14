import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Plus, Pencil, Trash2, RotateCcw, Eye } from 'lucide-react';
import toast from 'react-hot-toast';
import { PageHeader } from '@/components/common/PageHeader';
import { DataTable } from '@/components/common/DataTable';
import { StatusBadge } from '@/components/common/StatusBadge';
import { ConfirmDialog } from '@/components/common/ConfirmDialog';
import { doctorService } from '@/services/doctorService';
import { Doctor } from '@/types/doctor';
import { getErrorMessage } from '@/api/error';

export const DoctorsPage: React.FC = () => {
  const queryClient = useQueryClient();
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const [deleteId, setDeleteId] = useState<number | null>(null);
  const [restoreId, setRestoreId] = useState<number | null>(null);
  const limit = 10;

  const { data, isLoading, isError, refetch } = useQuery({
    queryKey: ['doctors', page, search],
    queryFn: () => doctorService.getAll({ page, limit, search }),
  });

  const deleteMutation = useMutation({
    mutationFn: doctorService.delete,
    onSuccess: () => {
      toast.success('Doctor deleted successfully');
      queryClient.invalidateQueries({ queryKey: ['doctors'] });
      setDeleteId(null);
    },
    onError: (error) => toast.error(getErrorMessage(error)),
  });

  const restoreMutation = useMutation({
    mutationFn: doctorService.restore,
    onSuccess: () => {
      toast.success('Doctor restored successfully');
      queryClient.invalidateQueries({ queryKey: ['doctors'] });
      setRestoreId(null);
    },
    onError: (error) => toast.error(getErrorMessage(error)),
  });

const [deleteId, setDeleteId] = useState<string | null>(null);
const [restoreId, setRestoreId] = useState<string | null>(null);

const columns = [
  { key: 'doctor_id', header: 'ID' },
  { key: 'full_name', header: 'Name' },
  { key: 'email', header: 'Email' },
  { key: 'department', header: 'Department' },
  { key: 'specialization', header: 'Specialization' },
  { key: 'status', header: 'Status', render: (item: Doctor) => <StatusBadge status={item.status} /> },
  {
    key: 'actions',
    header: 'Actions',
    render: (item: Doctor) => (
      <div className="flex items-center gap-2">
        <button className="p-1.5 text-gray-500 hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-colors" title="View"><Eye size={16} /></button>
        <button className="p-1.5 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors" title="Edit"><Pencil size={16} /></button>
        {item.is_active ? (
          <button onClick={() => setDeleteId(item.doctor_id)} className="p-1.5 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors" title="Delete"><Trash2 size={16} /></button>
        ) : (
          <button onClick={() => setRestoreId(item.doctor_id)} className="p-1.5 text-gray-500 hover:text-green-600 hover:bg-green-50 rounded-lg transition-colors" title="Restore"><RotateCcw size={16} /></button>
        )}
      </div>
    ),
  },
];

// keyExtractor:
keyExtractor={(item) => item.doctor_id}

  return (
    <div>
      <PageHeader title="Doctors" description="Manage hospital doctors" action={
        <button className="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg text-sm font-medium hover:bg-primary-700 transition-colors">
          <Plus size={18} /> Register Doctor
        </button>
      } />
      <DataTable columns={columns} data={data?.items ?? []} isLoading={isLoading} isError={isError} onRetry={refetch}
        searchPlaceholder="Search doctors..." onSearch={setSearch}
        pagination={{ page, limit, total: data?.total ?? 0, onPageChange: setPage }}
        keyExtractor={(item) => item.doctor_id} />
      <ConfirmDialog isOpen={!!deleteId} title="Delete Doctor" message="Are you sure you want to delete this doctor? This action can be reversed later."
        confirmText="Delete" confirmVariant="danger"
        onConfirm={() => deleteId && deleteMutation.mutate(deleteId)} onCancel={() => setDeleteId(null)} />
      <ConfirmDialog isOpen={!!restoreId} title="Restore Doctor" message="Are you sure you want to restore this doctor?"
        confirmText="Restore" confirmVariant="primary"
        onConfirm={() => restoreId && restoreMutation.mutate(restoreId)} onCancel={() => setRestoreId(null)} />
    </div>
  );
};
