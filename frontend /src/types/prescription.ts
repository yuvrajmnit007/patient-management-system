export interface Medicine {
  medicine_name: string;
  dosage: string;
  frequency: string;
  duration: string;
  instructions: string;
}

export interface Prescription {
  id: number;
  appointment_id: number;
  patient_id: number;
  doctor_id: number;
  diagnosis: string;
  medicines: Medicine[];
  advice?: string;
  follow_up_date?: string;
  appointment?: AppointmentSummary;
  patient?: PatientSummary;
  doctor?: DoctorSummary;
  is_active: boolean;
  created_at?: string;
  updated_at?: string;
}

export interface AppointmentSummary {
  id: number;
  appointment_date: string;
  appointment_time: string;
  status: string;
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

export interface PrescriptionCreateRequest {
  appointment_id: number;
  patient_id: number;
  doctor_id: number;
  diagnosis: string;
  medicines: Medicine[];
  advice?: string;
  follow_up_date?: string;
}

export interface PrescriptionUpdateRequest {
  diagnosis?: string;
  medicines?: Medicine[];
  advice?: string;
  follow_up_date?: string;
}

export interface PrescriptionFilters {
  search?: string;
  doctor_id?: number;
  patient_id?: number;
  page?: number;
  limit?: number;
}
