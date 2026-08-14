import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Plus, Pencil, Trash2, RotateCcw } from 'lucide-react';
import toast from 'react-hot-toast';
import { PageHeader } from '@/components/common/PageHeader';
import { DataTable } from '@/components/common/DataTable';
import { ConfirmDialog } from '@/components/common/ConfirmDialog';
import { patientService } from '@/services/patientService';
import { Patient } from '@/types/patient';
import { getErrorMessage } from '@/api/error';

export const PatientsPage: React.FC = () => {
  const queryClient = useQueryClient();
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const [deleteId, setDeleteId] = useState<number | null>(null);
  const [restoreId, setRestoreId] = useState<number | null>(null);
  const limit = 10;

  const { data, isLoading, isError, refetch } = useQuery({
    queryKey: ['patients', page, search],
    queryFn: () => patientService.getAll({ page, limit, search }),
  });

  const deleteMutation = useMutation({
    mutationFn: patientService.delete,
    onSuccess: () => {
      toast.success('Patient deleted successfully');
      queryClient.invalidateQueries({ queryKey: ['patients'] });
      setDeleteId(null);
    },
    onError: (error) => toast.error(getErrorMessage(error)),
  });

  const restoreMutation = useMutation({
    mutationFn: patientService.restore,
    onSuccess: () => {
      toast.success('Patient restored successfully');
      queryClient.invalidateQueries({ queryKey: ['patients'] });
      setRestoreId(null);
    },
    onError: (error) => toast.error(getErrorMessage(error)),
  });

  const columns = [
    { key: 'id', header: 'ID' },
    { key: 'full_name', header: 'Name' },
    { key: 'email', header: 'Email' },
    { key: 'phone_number', header: 'Phone' },
    { key: 'gender', header: 'Gender' },
    { key: 'blood_group', header: 'Blood Group' },
    {
      key: 'actions',
      header: 'Actions',
      render: (item: Patient) => (
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
      <PageHeader title="Patients" description="Manage hospital patients" action={
        <button className="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg text-sm font-medium hover:bg-primary-700 transition-colors">
          <Plus size={18} /> Add Patient
        </button>
      } />
      <DataTable columns={columns} data={data?.items ?? []} isLoading={isLoading} isError={isError} onRetry={refetch}
        searchPlaceholder="Search patients..." onSearch={setSearch}
        pagination={{ page, limit, total: data?.total ?? 0, onPageChange: setPage }}
        keyExtractor={(item) => item.id} />
      <ConfirmDialog isOpen={!!deleteId} title="Delete Patient" message="Are you sure you want to delete this patient?"
        confirmText="Delete" confirmVariant="danger"
        onConfirm={() => deleteId && deleteMutation.mutate(deleteId)} onCancel={() => setDeleteId(null)} />
      <ConfirmDialog isOpen={!!restoreId} title="Restore Patient" message="Are you sure you want to restore this patient?"
        confirmText="Restore" confirmVariant="primary"
        onConfirm={() => restoreId && restoreMutation.mutate(restoreId)} onCancel={() => setRestoreId(null)} />
    </div>
  );
};
