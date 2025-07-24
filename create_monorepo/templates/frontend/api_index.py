API_INDEX = """import axios, { 
    InternalAxiosRequestConfig, 
    AxiosResponse, 
    AxiosInstance 
} from "axios";
import { supabase } from '@/lib/supabase';


const createApiInstance = (withInterceptors: boolean = true) => {
    const api = axios.create({
        baseURL: process.env.NEXT_PUBLIC_API_BASE_URL,
        timeout: 30000,
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
    });

    if (withInterceptors) {
        // request interceptor to add auth token
        api.interceptors.request.use(
            async (config: InternalAxiosRequestConfig) => {
                try {
                    const { data: { session } } = await supabase.auth.getSession();
                    
                    if (session?.access_token) {
                        config.headers = config.headers || {};
                        config.headers.Authorization = `Bearer ${session.access_token}`;
                    }
                } catch (error) {
                    console.error('Error getting auth token:', error);
                }
                return config;
            },
            (error) => {
                return Promise.reject(error);
            }
        );

        // response interceptor to handle 401 errors
        api.interceptors.response.use(
            (response: AxiosResponse) => {
                return response;
            },
            async (error) => {
                if (error.response?.status === 401) {
                    // token expired or invalid
                    console.log('Token expired, logging out user...');
                    
                    // clear auth data
                    try {
                        await supabase.auth.signOut();
                        localStorage.removeItem('supabase.auth.token');
                        
                        // redirect to login page
                        if (typeof window !== 'undefined') {
                            window.location.href = '/';
                        }
                    } catch (logoutError) {
                        console.error('Error during logout:', logoutError);
                        // force redirect even if logout fails
                        if (typeof window !== 'undefined') {
                            window.location.href = '/';
                        }
                    }
                }
                return Promise.reject(error);
            }
        );
    }

    return api;
}

const api = createApiInstance(true);
const pubApi = createApiInstance(false);

const createApiClient = (instance: AxiosInstance) => ({
  get: async <T = unknown>(url: string, params?: Record<string, unknown>): Promise<T> => {
    const response: AxiosResponse<T> = await instance.get(url, { params });
    return response.data;
  },
  
  post: async <T = unknown>(url: string, data?: unknown): Promise<T> => {
    const response: AxiosResponse<T> = await instance.post(url, data);
    return response.data;
  },
  
  put: async <T = unknown>(url: string, data?: unknown): Promise<T> => {
    const response: AxiosResponse<T> = await instance.put(url, data);
    return response.data;
  },
  
  patch: async <T = unknown>(url: string, data?: unknown): Promise<T> => {
    const response: AxiosResponse<T> = await instance.patch(url, data);
    return response.data;
  },
  
  delete: async <T = unknown>(url: string): Promise<T> => {
    const response: AxiosResponse<T> = await instance.delete(url);
    return response.data;
  },
});

export const apiClient = createApiClient(api);
export const pubApiClient = createApiClient(pubApi);"""
