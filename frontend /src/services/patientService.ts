import api from '@/api/axios';
import {
  Patient,
  PatientCreateRequest,
  PatientUpdateRequest,
  PatientFilters,
} from '@/types/patient';
import { PaginatedResponse } from '@/types/common';

export const patientService = {
  create: async (data: PatientCreateRequest): Promise<Patient> => {
    const response = await api.post<Patient>('/patients', data);
    return response.data;
  },

  getAll: async (filters?: PatientFilters): Promise<PaginatedResponse<Patient>> => {
    const response = await api.get<PaginatedResponse<Patient>>('/patients', {
      params: filters,
    });
    return response.data;
  },

  getById: async (patientId: string): Promise<Patient> => {
    const response = await api.get<Patient>(`/patients/${patientId}`);
    return response.data;
  },

  update: async (
    patientId: string,
    data: PatientUpdateRequest,
  ): Promise<Patient> => {
    const response = await api.put<Patient>(`/patients/${patientId}`, data);
    return response.data;
  },

  delete: async (patientId: string): Promise<void> => {
    await api.delete(`/patients/${patientId}`);
  },

  restore: async (patientId: string): Promise<Patient> => {
    const response = await api.patch<Patient>(`/patients/${patientId}/restore`);
    return response.data;
  },
};