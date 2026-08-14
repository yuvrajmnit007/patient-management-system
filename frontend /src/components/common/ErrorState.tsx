import React from 'react';
import { AlertCircle } from 'lucide-react';

interface ErrorStateProps {
  message?: string;
  onRetry?: () => void;
}

export const ErrorState: React.FC<ErrorStateProps> = ({
  message = 'Something went wrong. Please try again.',
  onRetry,
}) => {
  return (
    <div className="flex flex-col items-center justify-center py-16 px-4">
      <div className="rounded-full bg-red-50 p-4 mb-4">
        <AlertCircle size={32} className="text-red-500" />
      </div>
      <h3 className="text-lg font-medium text-gray-900">Error</h3>
      <p className="mt-1 text-sm text-gray-500 text-center max-w-sm">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="mt-4 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors text-sm font-medium"
        >
          Try Again
        </button>
      )}
    </div>
  );
};
