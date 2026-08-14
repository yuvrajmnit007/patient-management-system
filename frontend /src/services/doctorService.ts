import api from '@/api/axios';
import {
  Doctor,
  DoctorRegistrationRequest,
  DoctorUpdateRequest,
  DoctorFilters,
} from '@/types/doctor';
import { PaginatedResponse } from '@/types/common';

export const doctorService = {
  register: async (data: DoctorRegistrationRequest): Promise<Doctor> => {
    const response = await api.post<Doctor>('/doctors/register', data);
    return response.data;
  },

  getAll: async (filters?: DoctorFilters): Promise<PaginatedResponse<Doctor>> => {
    const response = await api.get<PaginatedResponse<Doctor>>('/doctors', {
      params: filters,
    });
    return response.data;
  },

  getPending: async (): Promise<Doctor[]> => {
    const response = await api.get<Doctor[]>('/doctors/pending');
    return response.data;
  },

  getById: async (doctorId: string): Promise<Doctor> => {
    const response = await api.get<Doctor>(`/doctors/${doctorId}`);
    return response.data;
  },

  update: async (
    doctorId: string,
    data: DoctorUpdateRequest,
  ): Promise<Doctor> => {
    const response = await api.put<Doctor>(`/doctors/${doctorId}`, data);
    return response.data;
  },

  delete: async (doctorId: string): Promise<void> => {
    await api.delete(`/doctors/${doctorId}`);
  },

  restore: async (doctorId: string): Promise<Doctor> => {
    const response = await api.patch<Doctor>(`/doctors/${doctorId}/restore`);
    return response.data;
  },

  approve: async (doctorId: string): Promise<Doctor> => {
    const response = await api.patch<Doctor>(`/doctors/${doctorId}/approve`);
    return response.data;
  },

  reject: async (doctorId: string): Promise<Doctor> => {
    const response = await api.patch<Doctor>(`/doctors/${doctorId}/reject`);
    return response.data;
  },
};