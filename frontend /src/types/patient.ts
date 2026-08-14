export type Gender = 'male' | 'female' | 'other';

export type BloodGroup =
  | 'A+' | 'A-' | 'B+' | 'B-'
  | 'AB+' | 'AB-' | 'O+' | 'O-';

export interface Patient {
  id: number;
  patient_id: string;                    // e.g. "HM00000001"
  full_name: string;
  date_of_birth: string;                 // ISO date
  gender: Gender;
  blood_group?: BloodGroup | null;
  phone_number: string;
  email?: string | null;
  address?: string | null;
  emergency_contact_name?: string | null;
  emergency_contact_number?: string | null;
  allergies?: string | null;
  medical_history?: string | null;
  is_active: boolean;
  created_by?: number | null;
  created_at: string;
  updated_at: string;
}

export interface PatientCreateRequest {
  full_name: string;
  date_of_birth: string;
  gender: Gender;
  blood_group?: BloodGroup;
  phone_number: string;
  email?: string;
  address?: string;
  emergency_contact_name?: string;
  emergency_contact_number?: string;
  allergies?: string;
  medical_history?: string;
}

export type PatientUpdateRequest = Partial<PatientCreateRequest>;

export interface PatientFilters {
  search?: string;
  page?: number;
  limit?: number;
}