export type DoctorStatus = 'pending' | 'approved' | 'rejected';

export type Specialization =
  | 'Cardiology' | 'Dermatology' | 'Neurology' | 'Pediatrics'
  | 'Orthopedics' | 'Gynecology' | 'Psychiatry' | 'Oncology'
  | 'Radiology' | 'Urology' | 'Gastroenterology' | 'General Physician';

export type Department =
  | 'Medicine' | 'Surgery' | 'Emergency' | 'ICU'
  | 'ENT' | 'OPD' | 'Radiology' | 'Orthopedics';

export interface Doctor {
  id: number;
  doctor_id: string;                     // e.g. "DOC00000001"
  full_name: string;
  specialization: Specialization;
  department: Department;
  qualification: string;
  experience: number;
  consultation_fee: number;
  availability?: string | null;
  phone_number: string;
  email?: string | null;
  address?: string | null;
  is_active: boolean;
  status: DoctorStatus;
  created_by?: number | null;
  created_at: string;
  updated_at: string;
}

export interface DoctorRegistrationRequest {
  full_name: string;
  specialization: Specialization;
  department: Department;
  qualification: string;
  experience: number;
  consultation_fee: number;
  availability?: string;
  phone_number: string;
  email: string;                         // required per backend fix
  password: string;
  address?: string;
}

export type DoctorUpdateRequest = Partial
  Omit<DoctorRegistrationRequest, 'password' | 'email'>
> & { email?: string };

export interface DoctorFilters {
  search?: string;
  department?: Department;
  specialization?: Specialization;
  status?: DoctorStatus;
  page?: number;
  limit?: number;
}