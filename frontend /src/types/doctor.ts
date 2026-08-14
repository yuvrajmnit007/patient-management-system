export type DoctorStatus = 'Pending' | 'Approved' | 'Rejected';

export interface Doctor {
  id: number;
  full_name: string;
  specialization: string;
  department: string;
  qualification: string;
  experience: number;
  consultation_fee: number;
  availability: string;
  phone_number: string;
  email: string;
  address: string;
  status: DoctorStatus;
  is_active: boolean;
  user_id?: number;
  created_at?: string;
  updated_at?: string;
}

export interface DoctorRegistrationRequest {
  full_name: string;
  specialization: string;
  department: string;
  qualification: string;
  experience: number;
  consultation_fee: number;
  availability: string;
  phone_number: string;
  email: string;
  password: string;
  address: string;
}

export interface DoctorUpdateRequest {
  full_name?: string;
  specialization?: string;
  department?: string;
  qualification?: string;
  experience?: number;
  consultation_fee?: number;
  availability?: string;
  phone_number?: string;
  email?: string;
  address?: string;
}

export interface DoctorFilters {
  search?: string;
  department?: string;
  specialization?: string;
  status?: DoctorStatus;
  page?: number;
  limit?: number;
}
