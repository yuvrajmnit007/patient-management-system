import { AxiosError } from 'axios';

interface FieldError {
  loc?: (string | number)[];
  msg?: string;
  type?: string;
}

export interface ApiErrorResponse {
  detail?: string | FieldError[];
  message?: string;
}

const formatFieldError = (err: FieldError): string => {
  const field = err.loc?.slice(1).join('.') ?? 'field';
  return `${field}: ${err.msg ?? 'invalid'}`;
};

export const getErrorMessage = (error: unknown): string => {
  if (error instanceof AxiosError) {
    const data = error.response?.data as ApiErrorResponse | undefined;

    if (typeof data?.detail === 'string') return data.detail;

    if (Array.isArray(data?.detail)) {
      return data.detail.map(formatFieldError).join('; ');
    }

    if (data?.message) return data.message;

    switch (error.response?.status) {
      case 400: return 'Bad request. Please check your input.';
      case 403: return 'You do not have permission to perform this action.';
      case 404: return 'Resource not found.';
      case 422: return 'Validation error. Please check your input.';
      case 500: return 'Server error. Please try again later.';
      default:  return error.message || 'An unexpected error occurred.';
    }
  }
  if (error instanceof Error) return error.message;
  return 'An unexpected error occurred.';
};