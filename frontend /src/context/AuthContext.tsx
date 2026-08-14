import React, {
  createContext,
  useState,
  useEffect,
  useCallback,
} from 'react';
import { useNavigate } from 'react-router-dom';
import { jwtDecode } from 'jwt-decode';
import toast from 'react-hot-toast';

import { User, UserRole, AuthState } from '@/types/auth';
import { authService } from '@/services/authService';
import { getErrorMessage } from '@/api/error';

interface JwtPayload {
  sub: string;
  role?: UserRole;
  exp: number;
  iat: number;
}

export interface AuthContextType extends AuthState {
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  hasRole: (role: UserRole) => boolean;
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined);


export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const navigate = useNavigate();
  const [state, setState] = useState<AuthState>({
    user: null,
    token: null,
    isAuthenticated: false,
    isLoading: true,
  });

  const logout = useCallback(() => {
    localStorage.removeItem('hms_token');
    localStorage.removeItem('hms_user');
    setState({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,
    });
    navigate('/login', { replace: true });
  }, [navigate]);

  const initAuth = useCallback(async () => {
    const token = localStorage.getItem('hms_token');
    const storedUser = localStorage.getItem('hms_user');

    if (!token) {
      setState((prev) => ({ ...prev, isLoading: false }));
      return;
    }

    try {
      const decoded = jwtDecode<JwtPayload>(token);
      if (decoded.exp * 1000 < Date.now()) {
        logout();
        return;
      }

      const user = storedUser
        ? (JSON.parse(storedUser) as User)
        : await authService.getCurrentUser();

      if (!storedUser) {
        localStorage.setItem('hms_user', JSON.stringify(user));
      }

      setState({
        user,
        token,
        isAuthenticated: true,
        isLoading: false,
      });
    } catch {
      logout();
    }
  }, [logout]);

  useEffect(() => {
    initAuth();
  }, [initAuth]);

  const login = async (email: string, password: string) => {
    try {
      const { access_token } = await authService.login({ email, password });
      localStorage.setItem('hms_token', access_token);

      const user = await authService.getCurrentUser();
      localStorage.setItem('hms_user', JSON.stringify(user));

      setState({
        user,
        token: access_token,
        isAuthenticated: true,
        isLoading: false,
      });

      toast.success('Login successful');

      if (user.role === 'admin') {
        navigate('/admin/dashboard', { replace: true });
      } else if (user.role === 'doctor') {
        navigate('/doctor/dashboard', { replace: true });
      } else {
        navigate('/', { replace: true });
      }
    } catch (error) {
      toast.error(getErrorMessage(error));
      throw error;
    }
  };

  const hasRole = (role: UserRole): boolean => state.user?.role === role;

  return (
    <AuthContext.Provider value={{ ...state, login, logout, hasRole }}>
      {children}
    </AuthContext.Provider>
  );
};