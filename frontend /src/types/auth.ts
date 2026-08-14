export type UserRole = 'admin' | 'doctor' | 'receptionist';

export interface User {
  id: number;
  username: string;
  full_name: string;
  email: string;
  phone_number: string;
  role: UserRole;
  is_active: boolean;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}