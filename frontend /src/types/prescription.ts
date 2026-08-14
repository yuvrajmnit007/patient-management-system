export interface Medicine {
  medicine_name: string;
  dosage: string;
  frequency: string;
  duration: string;
  instructions?: string | null;
}

export interface Prescription {
  prescription_id: string;               // "PRS00000001"
  appointment_id: string;                // "APT00000001"
  diagnosis: string;
  advice?: string | null;
  follow_up_date?: string | null;
  medicines: Medicine[];
  is_active: boolean;
  created_by: number;
  created_at: string;
  updated_at: string;
}

export interface PrescriptionCreateRequest {
  appointment_id: string;
  diagnosis: string;
  advice?: string;
  follow_up_date?: string;
  medicines: Medicine[];
}

export interface PrescriptionUpdateRequest {
  diagnosis?: string;
  advice?: string;
  follow_up_date?: string;
  medicines?: Medicine[];
}

export interface PrescriptionFilters {
  search?: string;
  page?: number;
  limit?: number;
}