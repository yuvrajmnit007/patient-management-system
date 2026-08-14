import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { jwtDecode } from 'jwt-decode';
import { User, UserRole, AuthState } from '@/types/auth';
import { authService } from '@/services/authService';
import toast from 'react-hot-toast';

interface JwtPayload {
  sub: string;
  role?: UserRole;
  exp: number;
  iat: number;
}

interface AuthContextType extends AuthState {
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  hasRole: (role: UserRole) => boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
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
    window.location.href = '/login';
  }, []);

  const initAuth = useCallback(async () => {
    const token = localStorage.getItem('hms_token');
    const storedUser = localStorage.getItem('hms_user');

    if (!token) {
      setState((prev) => ({ ...prev, isLoading: false }));
      return;
    }

    try {
      // Check token expiration
      const decoded = jwtDecode<JwtPayload>(token);
      if (decoded.exp * 1000 < Date.now()) {
        logout();
        return;
      }

      if (storedUser) {
        const user = JSON.parse(storedUser) as User;
        setState({
          user,
          token,
          isAuthenticated: true,
          isLoading: false,
        });
      } else {
        // Fetch current user if not in localStorage
        const user = await authService.getCurrentUser();
        localStorage.setItem('hms_user', JSON.stringify(user));
        setState({
          user,
          token,
          isAuthenticated: true,
          isLoading: false,
        });
      }
    } catch {
      logout();
    }
  }, [logout]);

  useEffect(() => {
    initAuth();
  }, [initAuth]);

  const login = async (email: string, password: string) => {
    try {
      const response = await authService.login({ email, password });
      const { access_token } = response;
      localStorage.setItem('hms_token', access_token);

      const decoded = jwtDecode<JwtPayload>(access_token);

      // Fetch full user data
      const user = await authService.getCurrentUser();
      localStorage.setItem('hms_user', JSON.stringify(user));

      setState({
        user,
        token: access_token,
        isAuthenticated: true,
        isLoading: false,
      });

      toast.success('Login successful');

      // Redirect based on role
      if (user.role === 'ADMIN') {
        window.location.href = '/admin/dashboard';
      } else if (user.role === 'DOCTOR') {
        window.location.href = '/doctor/dashboard';
      }
    } catch (error) {
      toast.error('Invalid email or password');
      throw error;
    }
  };

  const hasRole = (role: UserRole): boolean => {
    return state.user?.role === role;
  };

  return (
    <AuthContext.Provider value={{ ...state, login, logout, hasRole }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
