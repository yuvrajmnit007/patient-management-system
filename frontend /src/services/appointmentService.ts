import api from '@/api/axios';
import {
  Appointment,
  AppointmentCreateRequest,
  AppointmentUpdateRequest,
  AppointmentFilters,
} from '@/types/appointment';
import { PaginatedResponse } from './doctorService';

export const appointmentService = {
  create: async (data: AppointmentCreateRequest): Promise<Appointment> => {
    const response = await api.post<Appointment>('/appointments', data);
    return response.data;
  },

  getAll: async (filters?: AppointmentFilters): Promise<PaginatedResponse<Appointment>> => {
    const response = await api.get<PaginatedResponse<Appointment>>('/appointments', {
      params: filters,
    });
    return response.data;
  },

  getById: async (id: number): Promise<Appointment> => {
    const response = await api.get<Appointment>(`/appointments/${id}`);
    return response.data;
  },

  update: async (id: number, data: AppointmentUpdateRequest): Promise<Appointment> => {
    const response = await api.put<Appointment>(`/appointments/${id}`, data);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/appointments/${id}`);
  },

  restore: async (id: number): Promise<Appointment> => {
    const response = await api.patch<Appointment>(`/appointments/restore/${id}`);
    return response.data;
  },

  confirm: async (id: number): Promise<Appointment> => {
    const response = await api.patch<Appointment>(`/appointments/confirm/${id}`);
    return response.data;
  },
};
