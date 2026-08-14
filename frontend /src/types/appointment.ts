export type AppointmentStatus =
  | 'Pending' | 'Confirmed' | 'In Progress'
  | 'Completed' | 'Cancelled' | 'No Show';

export interface Appointment {
  appointment_id: string;                // "APT00000001"
  patient_id: string;                    // "HM00000001"
  patient_name: string;
  doctor_id: string;                     // "DOC00000001"
  doctor_name: string;
  appointment_date: string;              // ISO date
  appointment_time: string;              // HH:MM:SS
  reason: string;
  notes?: string | null;
  status: AppointmentStatus;
  is_active: boolean;
  created_by: number;
  created_at: string;
  updated_at: string;
}

export interface AppointmentCreateRequest {
  patient_id: string;
  doctor_id: string;
  appointment_date: string;
  appointment_time: string;
  reason: string;
  notes?: string;
}

export interface AppointmentUpdateRequest {
  appointment_date?: string;
  appointment_time?: string;
  reason?: string;
  notes?: string;
  status?: AppointmentStatus;
}

export interface AppointmentFilters {
  search?: string;
  appointment_status?: AppointmentStatus;
  doctor_id?: string;
  patient_id?: string;
  appointment_date?: string;
  page?: number;
  limit?: number;
}export type AppointmentStatus =
  | 'Pending' | 'Confirmed' | 'In Progress'
  | 'Completed' | 'Cancelled' | 'No Show';

export interface Appointment {
  appointment_id: string;                // "APT00000001"
  patient_id: string;                    // "HM00000001"
  patient_name: string;
  doctor_id: string;                     // "DOC00000001"
  doctor_name: string;
  appointment_date: string;              // ISO date
  appointment_time: string;              // HH:MM:SS
  reason: string;
  notes?: string | null;
  status: AppointmentStatus;
  is_active: boolean;
  created_by: number;
  created_at: string;
  updated_at: string;
}

export interface AppointmentCreateRequest {
  patient_id: string;
  doctor_id: string;
  appointment_date: string;
  appointment_time: string;
  reason: string;
  notes?: string;
}

export interface AppointmentUpdateRequest {
  appointment_date?: string;
  appointment_time?: string;
  reason?: string;
  notes?: string;
  status?: AppointmentStatus;
}

export interface AppointmentFilters {
  search?: string;
  appointment_status?: AppointmentStatus;
  doctor_id?: string;
  patient_id?: string;
  appointment_date?: string;
  page?: number;
  limit?: number;
}