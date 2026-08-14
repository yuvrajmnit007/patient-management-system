import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Eye } from 'lucide-react';
import { PageHeader } from '@/components/common/PageHeader';
import { DataTable } from '@/components/common/DataTable';
import { prescriptionService } from '@/services/prescriptionService';
import { Prescription } from '@/types/prescription';

export const PrescriptionsPage: React.FC = () => {
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const limit = 10;

  const { data, isLoading, isError, refetch } = useQuery({
    queryKey: ['prescriptions', page, search],
    queryFn: () => prescriptionService.getAll({ page, limit, search }),
  });

  const columns = [
    { key: 'id', header: 'Prescription ID' },
    { key: 'patient', header: 'Patient', render: (item: Prescription) => item.patient?.full_name || '-' },
    { key: 'doctor', header: 'Doctor', render: (item: Prescription) => item.doctor?.full_name || '-' },
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
      <PageHeader title="Prescriptions" description="View all prescriptions" />
      <DataTable columns={columns} data={data?.items ?? []} isLoading={isLoading} isError={isError} onRetry={refetch}
        searchPlaceholder="Search prescriptions..." onSearch={setSearch}
        pagination={{ page, limit, total: data?.total ?? 0, onPageChange: setPage }}
        keyExtractor={(item) => item.id} />
    </div>
  );
};
