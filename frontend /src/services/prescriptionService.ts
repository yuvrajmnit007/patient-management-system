import api from '@/api/axios';
import {
  Prescription,
  PrescriptionCreateRequest,
  PrescriptionUpdateRequest,
  PrescriptionFilters,
} from '@/types/prescription';
import { PaginatedResponse } from '@/types/common';

export const prescriptionService = {
  create: async (data: PrescriptionCreateRequest): Promise<Prescription> => {
    const response = await api.post<Prescription>('/prescriptions', data);
    return response.data;
  },

  getAll: async (
    filters?: PrescriptionFilters,
  ): Promise<PaginatedResponse<Prescription>> => {
    const response = await api.get<PaginatedResponse<Prescription>>(
      '/prescriptions',
      { params: filters },
    );
    return response.data;
  },

  getById: async (prescriptionId: string): Promise<Prescription> => {
    const response = await api.get<Prescription>(
      `/prescriptions/${prescriptionId}`,
    );
    return response.data;
  },

  update: async (
    prescriptionId: string,
    data: PrescriptionUpdateRequest,
  ): Promise<Prescription> => {
    const response = await api.put<Prescription>(
      `/prescriptions/${prescriptionId}`,
      data,
    );
    return response.data;
  },

  delete: async (prescriptionId: string): Promise<void> => {
    await api.delete(`/prescriptions/${prescriptionId}`);
  },

  restore: async (prescriptionId: string): Promise<Prescription> => {
    const response = await api.patch<Prescription>(
      `/prescriptions/${prescriptionId}/restore`,
    );
    return response.data;
  },
};