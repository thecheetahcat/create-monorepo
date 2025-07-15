USE_AUTH = """import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { User } from '@supabase/supabase-js';
import { supabase } from '@/lib/supabase';

interface UseAuthReturn {
  user: User | null;
  logout: () => Promise<void>;
}

export function useAuth(redirectPath: string = '/'): UseAuthReturn {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        // get the current session - this validates the token
        const { data: { session }, error } = await supabase.auth.getSession();
        
        if (error || !session || !session.user) {
          // no valid session, redirect to login
          router.push(redirectPath);
          return;
        }
        
        // check if token is expired
        const now = Math.floor(Date.now() / 1000);
        if (session.expires_at && session.expires_at < now) {
          // token expired, clear and redirect
          await supabase.auth.signOut();
          localStorage.removeItem('supabase.auth.token');
          router.push(redirectPath);
          return;
        }
        
        // valid session, set user
        setUser(session.user);
      } catch (error) {
        console.error('Auth check failed:', error);
        router.push(redirectPath);
        // why no return here but returns above?
      }
    };

    checkAuth();
  }, [router, redirectPath]);

  const logout = async () => {
    await supabase.auth.signOut();
    localStorage.removeItem('supabase.auth.token');
    router.push(redirectPath);
  };

  return { user, logout };
}"""
