import api from '@/api/axios';
import {
  Appointment,
  AppointmentCreateRequest,
  AppointmentUpdateRequest,
  AppointmentFilters,
} from '@/types/appointment';
import { PaginatedResponse } from '@/types/common';

export const appointmentService = {
  create: async (data: AppointmentCreateRequest): Promise<Appointment> => {
    const response = await api.post<Appointment>('/appointments', data);
    return response.data;
  },

  getAll: async (
    filters?: AppointmentFilters,
  ): Promise<PaginatedResponse<Appointment>> => {
    const response = await api.get<PaginatedResponse<Appointment>>(
      '/appointments',
      { params: filters },
    );
    return response.data;
  },

  getById: async (appointmentId: string): Promise<Appointment> => {
    const response = await api.get<Appointment>(
      `/appointments/${appointmentId}`,
    );
    return response.data;
  },

  update: async (
    appointmentId: string,
    data: AppointmentUpdateRequest,
  ): Promise<Appointment> => {
    const response = await api.put<Appointment>(
      `/appointments/${appointmentId}`,
      data,
    );
    return response.data;
  },

  delete: async (appointmentId: string): Promise<void> => {
    await api.delete(`/appointments/${appointmentId}`);
  },

  restore: async (appointmentId: string): Promise<Appointment> => {
    const response = await api.patch<Appointment>(
      `/appointments/${appointmentId}/restore`,
    );
    return response.data;
  },

  confirm: async (appointmentId: string): Promise<Appointment> => {
    const response = await api.patch<Appointment>(
      `/appointments/${appointmentId}/confirm`,
    );
    return response.data;
  },
};