import React from 'react';
import { AppointmentStatus, DoctorStatus } from '@/types';

type StatusType = AppointmentStatus | DoctorStatus | string;

interface StatusBadgeProps {
  status: StatusType;
}

const statusStyles: Record<string, string> = {
  // Doctor statuses
  Pending: 'bg-yellow-100 text-yellow-800 border-yellow-200',
  Approved: 'bg-green-100 text-green-800 border-green-200',
  Rejected: 'bg-red-100 text-red-800 border-red-200',
  // Appointment statuses
  Confirmed: 'bg-blue-100 text-blue-800 border-blue-200',
  'In Progress': 'bg-purple-100 text-purple-800 border-purple-200',
  Completed: 'bg-green-100 text-green-800 border-green-200',
  Cancelled: 'bg-gray-100 text-gray-800 border-gray-200',
  'No Show': 'bg-red-100 text-red-800 border-red-200',
};

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status }) => {
  const style = statusStyles[status] || 'bg-gray-100 text-gray-800 border-gray-200';

  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${style}`}
    >
      {status}
    </span>
  );
};
