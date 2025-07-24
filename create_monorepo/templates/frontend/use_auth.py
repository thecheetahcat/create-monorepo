USE_AUTH = """import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { User } from '@supabase/supabase-js';
import { supabase } from '@/lib/supabase';
import { profileApi } from '@/api/profiles/profileApi';

interface Profile {
  user_id: string;
  first_name?: string;
  last_name?: string;
}

interface UseAuthReturn {
  user: User | null;
  profile: Profile | null;
  logout: () => Promise<void>;
}

export function useAuth(redirectPath: string = '/'): UseAuthReturn {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [profile, setProfile] = useState<Profile | null>(null);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const { data: { session }, error } = await supabase.auth.getSession();
        if (error || !session || !session.user) {
          router.push(redirectPath);
          return;
        }

        const now = Math.floor(Date.now() / 1000);
        if (session.expires_at && session.expires_at < now) {
          await supabase.auth.signOut();
          localStorage.removeItem('supabase.auth.token');
          router.push(redirectPath);
          return;
        }
        
        setUser(session.user);

        const { status, first_name, last_name } = await profileApi.getProfile(session.user.id);
        if (status === 'success') {
          setProfile({
            user_id: session.user.id,
            first_name,
            last_name,
          });
        }
      } catch (error) {
        console.error('Auth check failed:', error);
        router.push(redirectPath);
      }
    };

    checkAuth();
  }, [router, redirectPath]);

  const logout = async () => {
    await supabase.auth.signOut();
    localStorage.removeItem('supabase.auth.token');
    router.push(redirectPath);
  };

  return { user, profile, logout };
}"""
