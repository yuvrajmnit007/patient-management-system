export interface Patient {
  id: number;
  full_name: string;
  email: string;
  phone_number: string;
  date_of_birth: string;
  gender: string;
  address: string;
  blood_group?: string;
  emergency_contact?: string;
  medical_history?: string;
  is_active: boolean;
  created_at?: string;
  updated_at?: string;
}

export interface PatientCreateRequest {
  full_name: string;
  email: string;
  phone_number: string;
  date_of_birth: string;
  gender: string;
  address: string;
  blood_group?: string;
  emergency_contact?: string;
  medical_history?: string;
}

export interface PatientUpdateRequest {
  full_name?: string;
  email?: string;
  phone_number?: string;
  date_of_birth?: string;
  gender?: string;
  address?: string;
  blood_group?: string;
  emergency_contact?: string;
  medical_history?: string;
}

export interface PatientFilters {
  search?: string;
  page?: number;
  limit?: number;
}
