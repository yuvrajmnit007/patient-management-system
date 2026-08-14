import api from '@/api/axios';
import {
  Patient,
  PatientCreateRequest,
  PatientUpdateRequest,
  PatientFilters,
} from '@/types/patient';
import { PaginatedResponse } from './doctorService';

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

  getById: async (id: number): Promise<Patient> => {
    const response = await api.get<Patient>(`/patients/${id}`);
    return response.data;
  },

  update: async (id: number, data: PatientUpdateRequest): Promise<Patient> => {
    const response = await api.put<Patient>(`/patients/${id}`, data);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/patients/${id}`);
  },

  restore: async (id: number): Promise<Patient> => {
    const response = await api.patch<Patient>(`/patients/restore/${id}`);
    return response.data;
  },
};
