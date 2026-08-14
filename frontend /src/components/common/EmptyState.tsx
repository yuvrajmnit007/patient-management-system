import React from 'react';
import { Inbox } from 'lucide-react';

interface EmptyStateProps {
  title?: string;
  description?: string;
  icon?: React.ReactNode;
  action?: React.ReactNode;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  title = 'No data found',
  description = 'There are no items to display at the moment.',
  icon,
  action,
}) => {
  return (
    <div className="flex flex-col items-center justify-center py-16 px-4">
      <div className="rounded-full bg-primary-50 p-4 mb-4">
        {icon || <Inbox size={32} className="text-primary-500" />}
      </div>
      <h3 className="text-lg font-medium text-gray-900">{title}</h3>
      <p className="mt-1 text-sm text-gray-500 text-center max-w-sm">{description}</p>
      {action && <div className="mt-4">{action}</div>}
    </div>
  );
};
