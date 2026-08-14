import api from '@/api/axios';
import {
  Doctor,
  DoctorRegistrationRequest,
  DoctorUpdateRequest,
  DoctorFilters,
} from '@/types/doctor';

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
  total_pages: number;
}

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

  getById: async (id: number): Promise<Doctor> => {
    const response = await api.get<Doctor>(`/doctors/${id}`);
    return response.data;
  },

  update: async (id: number, data: DoctorUpdateRequest): Promise<Doctor> => {
    const response = await api.put<Doctor>(`/doctors/${id}`, data);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/doctors/${id}`);
  },

  restore: async (id: number): Promise<Doctor> => {
    const response = await api.patch<Doctor>(`/doctors/restore/${id}`);
    return response.data;
  },

  getPending: async (): Promise<Doctor[]> => {
    const response = await api.get<Doctor[]>('/doctors/pending');
    return response.data;
  },

  approve: async (id: number): Promise<Doctor> => {
    const response = await api.patch<Doctor>(`/doctors/approve/${id}`);
    return response.data;
  },

  reject: async (id: number): Promise<Doctor> => {
    const response = await api.patch<Doctor>(`/doctors/reject/${id}`);
    return response.data;
  },
};
