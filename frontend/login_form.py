LOGIN_FORM = """'use client';

import { useState } from 'react';
import { supabase } from '@/lib/supabase';
import { useRouter } from 'next/navigation';

export default function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    const { data, error } = await supabase.auth.signInWithPassword({ email, password });
    if (error) {
      setError(error.message);
    } else {
      if (data.session) {
        localStorage.setItem('supabase.auth.token', JSON.stringify(data.session));
      }
      router.push('/your-redirect');
    }
  };

  return (
    <div className='min-h-screen flex items-center justify-center bg-gray-100 text-gray-900'>
      <form onSubmit={handleLogin} className='p-8 bg-white rounded shadow-md border border-gray-200 w-full max-w-sm'>
        <h2 className='text-2xl mb-4 text-center'>Login</h2>
        {error && <p className='text-red-500 mb-4'>{error}</p>}
        <input
          type='email'
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder='Email'
          className='mb-4 p-2 border w-full text-gray-900 bg-white'
          required
        />
        <input
          type='password'
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder='Password'
          className='mb-4 p-2 border w-full text-gray-900 bg-white'
          required
        />
        <button type='submit' className='bg-blue-600 text-white hover:bg-blue-700 p-2 w-full transition-colors'>
          Log In
        </button>
      </form>
    </div>
  );
}
"""
