import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Eye } from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';
import { PageHeader } from '@/components/common/PageHeader';
import { DataTable } from '@/components/common/DataTable';
import { prescriptionService } from '@/services/prescriptionService';
import { Prescription } from '@/types/prescription';

export const MyPrescriptionsPage: React.FC = () => {
  const { user } = useAuth();
  const [page, setPage] = useState(1);
  const limit = 10;

  const { data, isLoading, isError, refetch } = useQuery({
    queryKey: ['prescriptions', 'my', page],
    queryFn: () => prescriptionService.getAll({ doctor_id: user?.id, page, limit }),
    enabled: !!user?.id,
  });

  const columns = [
    { key: 'id', header: 'ID' },
    { key: 'patient', header: 'Patient', render: (item: Prescription) => item.patient?.full_name || '-' },
    { key: 'diagnosis', header: 'Diagnosis' },
    { key: 'medicines', header: 'Medicines', render: (item: Prescription) => `${item.medicines.length} item(s)` },
    { key: 'created_at', header: 'Created' },
    {
      key: 'actions',
      header: 'Actions',
      render: (item: Prescription) => (
        <button className="p-1.5 text-gray-500 hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-colors">
          <Eye size={16} />
        </button>
      ),
    },
  ];

  return (
    <div>
      <PageHeader title="My Prescriptions" description="Prescriptions you have created" />
      <DataTable columns={columns} data={data?.items ?? []} isLoading={isLoading} isError={isError} onRetry={refetch}
        pagination={{ page, limit, total: data?.total ?? 0, onPageChange: setPage }}
        keyExtractor={(item) => item.id} />
    </div>
  );
};
