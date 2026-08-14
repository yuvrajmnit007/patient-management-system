import React from 'react';
import { Loader2 } from 'lucide-react';

interface LoadingSpinnerProps {
  size?: number;
  className?: string;
  text?: string;
}

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  size = 24,
  className = '',
  text = 'Loading...',
}) => {
  return (
    <div className={`flex flex-col items-center justify-center py-12 ${className}`}>
      <Loader2 size={size} className="animate-spin text-primary-600" />
      {text && <p className="mt-3 text-sm text-gray-500">{text}</p>}
    </div>
  );
};
