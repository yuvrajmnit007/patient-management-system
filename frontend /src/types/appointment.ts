export type AppointmentStatus = 'Pending' | 'Confirmed' | 'In Progress' | 'Completed' | 'Cancelled' | 'No Show';

export interface Appointment {
  id: number;
  patient_id: number;
  doctor_id: number;
  appointment_date: string;
  appointment_time: string;
  reason: string;
  status: AppointmentStatus;
  notes?: string;
  patient?: PatientSummary;
  doctor?: DoctorSummary;
  is_active: boolean;
  created_at?: string;
  updated_at?: string;
}

export interface PatientSummary {
  id: number;
  full_name: string;
  email: string;
  phone_number: string;
}

export interface DoctorSummary {
  id: number;
  full_name: string;
  specialization: string;
  department: string;
}

export interface AppointmentCreateRequest {
  patient_id: number;
  doctor_id: number;
  appointment_date: string;
  appointment_time: string;
  reason: string;
  notes?: string;
}

export interface AppointmentUpdateRequest {
  patient_id?: number;
  doctor_id?: number;
  appointment_date?: string;
  appointment_time?: string;
  reason?: string;
  status?: AppointmentStatus;
  notes?: string;
}

export interface AppointmentFilters {
  search?: string;
  status?: AppointmentStatus;
  doctor_id?: number;
  patient_id?: number;
  date_from?: string;
  date_to?: string;
  page?: number;
  limit?: number;
}
