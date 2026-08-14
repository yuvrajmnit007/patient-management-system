import { useQuery } from '@tanstack/react-query';
import api from '@/api/axios';
import { Doctor } from '@/types/doctor';
import { useAuth } from '@/hooks/useAuth';

export const useCurrentDoctor = () => {
  const { user } = useAuth();
  return useQuery({
    queryKey: ['doctor', 'me', user?.id],
    queryFn: async () => (await api.get<Doctor>('/doctors/me')).data,
    enabled: !!user && user.role === 'doctor',
    staleTime: 5 * 60 * 1000,
  });
};