import { AxiosError } from 'axios';

export interface ApiErrorResponse {
  detail?: string;
  message?: string;
  errors?: Record<string, string[]>;
}

export const getErrorMessage = (error: unknown): string => {
  if (error instanceof AxiosError) {
    const data = error.response?.data as ApiErrorResponse | undefined;
    if (data?.detail) return data.detail;
    if (data?.message) return data.message;
    if (error.response?.status === 400) return 'Bad request. Please check your input.';
    if (error.response?.status === 403) return 'You do not have permission to perform this action.';
    if (error.response?.status === 404) return 'Resource not found.';
    if (error.response?.status === 422) return 'Validation error. Please check your input.';
    if (error.response?.status === 500) return 'Server error. Please try again later.';
    return error.message || 'An unexpected error occurred.';
  }
  if (error instanceof Error) return error.message;
  return 'An unexpected error occurred.';
};
