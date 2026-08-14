import React, { useState } from 'react';
import { ChevronLeft, ChevronRight, Search } from 'lucide-react';
import { LoadingSpinner } from './LoadingSpinner';
import { EmptyState } from './EmptyState';
import { ErrorState } from './ErrorState';

export interface Column<T> {
  key: string;
  header: string;
  render?: (item: T) => React.ReactNode;
  width?: string;
}

interface DataTableProps<T> {
  columns: Column<T>[];
  data: T[];
  isLoading: boolean;
  isError: boolean;
  errorMessage?: string;
  onRetry?: () => void;
  searchPlaceholder?: string;
  onSearch?: (query: string) => void;
  searchValue?: string;
  pagination?: {
    page: number;
    limit: number;
    total: number;
    onPageChange: (page: number) => void;
    onLimitChange?: (limit: number) => void;
  };
  keyExtractor: (item: T) => string | number;
  emptyTitle?: string;
  emptyDescription?: string;
}

export function DataTable<T>({
  columns,
  data,
  isLoading,
  isError,
  errorMessage,
  onRetry,
  searchPlaceholder = 'Search...',
  onSearch,
  searchValue = '',
  pagination,
  keyExtractor,
  emptyTitle,
  emptyDescription,
}: DataTableProps<T>) {
  const [localSearch, setLocalSearch] = useState(searchValue);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch?.(localSearch);
  };

  const totalPages = pagination ? Math.ceil(pagination.total / pagination.limit) : 1;

  if (isLoading) {
    return <LoadingSpinner />;
  }

  if (isError) {
    return <ErrorState message={errorMessage} onRetry={onRetry} />;
  }

  return (
    <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
      {onSearch && (
        <div className="p-4 border-b border-gray-200">
          <form onSubmit={handleSearch} className="relative max-w-md">
            <Search
              size={18}
              className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
            />
            <input
              type="text"
              value={localSearch}
              onChange={(e) => setLocalSearch(e.target.value)}
              placeholder={searchPlaceholder}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </form>
        </div>
      )}

      <div className="overflow-x-auto">
        <table className="w-full text-sm text-left">
          <thead className="bg-gray-50 text-gray-700 font-medium">
            <tr>
              {columns.map((col) => (
                <th
                  key={col.key}
                  className="px-6 py-3.5 whitespace-nowrap"
                  style={col.width ? { width: col.width } : undefined}
                >
                  {col.header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {data.length === 0 ? (
              <tr>
                <td colSpan={columns.length} className="py-8">
                  <EmptyState
                    title={emptyTitle || 'No data found'}
                    description={emptyDescription || 'There are no items to display.'}
                  />
                </td>
              </tr>
            ) : (
              data.map((item) => (
                <tr
                  key={keyExtractor(item)}
                  className="hover:bg-gray-50 transition-colors"
                >
                  {columns.map((col) => (
                    <td key={col.key} className="px-6 py-4 whitespace-nowrap">
                      {col.render
                        ? col.render(item)
                        : (item as Record<string, unknown>)[col.key] as React.ReactNode}
                    </td>
                  ))}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {pagination && totalPages > 1 && (
        <div className="flex items-center justify-between px-6 py-4 border-t border-gray-200 bg-gray-50">
          <div className="text-sm text-gray-500">
            Showing {(pagination.page - 1) * pagination.limit + 1} to{' '}
            {Math.min(pagination.page * pagination.limit, pagination.total)} of{' '}
            {pagination.total} results
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => pagination.onPageChange(pagination.page - 1)}
              disabled={pagination.page <= 1}
              className="p-2 rounded-lg border border-gray-300 bg-white text-gray-600 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <ChevronLeft size={16} />
            </button>
            <span className="text-sm text-gray-700">
              Page {pagination.page} of {totalPages}
            </span>
            <button
              onClick={() => pagination.onPageChange(pagination.page + 1)}
              disabled={pagination.page >= totalPages}
              className="p-2 rounded-lg border border-gray-300 bg-white text-gray-600 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <ChevronRight size={16} />
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
