LOGIN_FORM = """'use client';

import { useState } from 'react';
import { supabase } from '@/lib/supabase';
import { useRouter } from 'next/navigation';
import { useMutation } from '@tanstack/react-query';
import { profileApi } from '@/api/profiles/profileApi';
import { Profile } from '@/api/profiles/profileApiTypes';

export default function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isSignUp, setIsSignUp] = useState(false);
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const router = useRouter();

  const createProfile = useMutation({
    mutationFn: (profile: Profile) => profileApi.createProfile(profile),
    onSuccess: () => {
      console.log('Profile created successfully');
      // TODO:
      // add something here to prompt them to confirm their email and then log back in
      router.push('/dashboard');
    },
    onError: (error) => {
      console.error('Error creating profile:', error);
      setError(error.message);
    },
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    try {
      if (isSignUp) {
        const { data, error } = await supabase.auth.signUp({ email, password });
        if (error) throw error;
        if (data.user) {
          createProfile.mutate({
            user_id: data.user.id,
            email: email,
            first_name: firstName || '',
            last_name: lastName || '',
          });
        }
      } else {
        const { data, error } = await supabase.auth.signInWithPassword({ email, password });
        if (error) throw error;
        if (data.session) {
          localStorage.setItem('supabase.auth.token', JSON.stringify(data.session));
          router.push('/dashboard');
        }
      }
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div className='min-h-screen flex items-center justify-center bg-gray-900 text-[#fafafa]'>
      <form onSubmit={handleSubmit} className='p-8 bg-gray-800 rounded shadow-md border border-gray-700 w-full max-w-sm'>
        <h2 className='text-2xl mb-4 text-center'>{isSignUp ? 'Sign Up' : 'Login'}</h2>
        {error && <p className='text-red-400 mb-4'>{error}</p>}
        <input
          type='email'
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder='Email'
          className='mb-4 p-2 border border-gray-600 w-full bg-gray-700 placeholder-gray-400 text-[#fafafa]'
          required
        />
        {isSignUp && (
          <>
            <input
              type='text'
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              placeholder='First Name'
              className='mb-4 p-2 border border-gray-600 w-full bg-gray-700 placeholder-gray-400 text-[#fafafa]'
              required
            />
            <input
              type='text'
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
              placeholder='Last Name'
              className='mb-4 p-2 border border-gray-600 w-full bg-gray-700 placeholder-gray-400 text-[#fafafa]'
              required
            />
          </>
        )}
        <input
          type='password'
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder='Password'
          className='mb-4 p-2 border border-gray-600 w-full bg-gray-700 placeholder-gray-400 text-[#fafafa]'
          required
        />
        <button type='submit' className='bg-gray-600 text-white hover:bg-gray-500 p-2 w-full transition-colors'>
          {isSignUp ? 'Sign Up' : 'Log In'}
        </button>
        <p className='mt-4 text-center'>
          {isSignUp ? 'Already have an account?' : 'Need an account?'}{' '}
          <button type='button' onClick={() => setIsSignUp(!isSignUp)} className='text-blue-400 hover:underline'>
            {isSignUp ? 'Log In' : 'Sign Up'}
          </button>
        </p>
      </form>
    </div>
  );
}
"""
