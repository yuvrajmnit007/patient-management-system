import api from '@/api/axios';
import {
  Prescription,
  PrescriptionCreateRequest,
  PrescriptionUpdateRequest,
  PrescriptionFilters,
} from '@/types/prescription';
import { PaginatedResponse } from './doctorService';

export const prescriptionService = {
  create: async (data: PrescriptionCreateRequest): Promise<Prescription> => {
    const response = await api.post<Prescription>('/prescriptions', data);
    return response.data;
  },

  getAll: async (filters?: PrescriptionFilters): Promise<PaginatedResponse<Prescription>> => {
    const response = await api.get<PaginatedResponse<Prescription>>('/prescriptions', {
      params: filters,
    });
    return response.data;
  },

  getById: async (id: number): Promise<Prescription> => {
    const response = await api.get<Prescription>(`/prescriptions/${id}`);
    return response.data;
  },

  update: async (id: number, data: PrescriptionUpdateRequest): Promise<Prescription> => {
    const response = await api.put<Prescription>(`/prescriptions/${id}`, data);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/prescriptions/${id}`);
  },

  restore: async (id: number): Promise<Prescription> => {
    const response = await api.patch<Prescription>(`/prescriptions/restore/${id}`);
    return response.data;
  },
};
