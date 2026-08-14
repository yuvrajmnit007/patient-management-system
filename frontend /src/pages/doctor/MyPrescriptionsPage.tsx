import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Eye } from 'lucide-react';

import { PageHeader } from '@/components/common/PageHeader';
import { DataTable } from '@/components/common/DataTable';
import { useCurrentDoctor } from '@/hooks/useCurrentDoctor';
import { prescriptionService } from '@/services/prescriptionService';
import { Prescription } from '@/types/prescription';

export const MyPrescriptionsPage: React.FC = () => {
  const doctorQ = useCurrentDoctor();
  const doctorId = doctorQ.data?.doctor_id;

  const [page, setPage] = useState(1);
  const limit = 10;

  const { data, isLoading, isError, refetch } = useQuery({
    queryKey: ['prescriptions', 'my', doctorId, page],
    queryFn: () =>
      prescriptionService.getAll({ doctor_id: doctorId, page, limit }),
    enabled: !!doctorId,
  });

  const columns = [
    { key: 'prescription_id', header: 'ID' },
    { key: 'appointment_id', header: 'Appointment' },
    { key: 'diagnosis', header: 'Diagnosis' },
    {
      key: 'medicines',
      header: 'Medicines',
      render: (item: Prescription) => `${item.medicines.length} item(s)`,
    },
    {
      key: 'created_at',
      header: 'Created',
      render: (item: Prescription) =>
        new Date(item.created_at).toLocaleDateString(),
    },
    {
      key: 'actions',
      header: 'Actions',
      render: () => (
        <button className="p-1.5 text-gray-500 hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-colors">
          <Eye size={16} />
        </button>
      ),
    },
  ];

  return (
    <div>
      <PageHeader
        title="My Prescriptions"
        description="Prescriptions you have created"
      />
      <DataTable
        columns={columns}
        data={data?.items ?? []}
        isLoading={isLoading || doctorQ.isLoading}
        isError={isError || doctorQ.isError}
        onRetry={refetch}
        pagination={{ page, limit, total: data?.total ?? 0, onPageChange: setPage }}
        keyExtractor={(item) => item.prescription_id}
      />
    </div>
  );
};