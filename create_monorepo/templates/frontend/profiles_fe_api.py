PROFILES_FE_API = """import { apiClient, pubApiClient } from '@/api/index';
import { Profile, ProfileResponse, UpdateProfile } from '@/api/profiles/profileApiTypes';

export const profileApi = {
    createProfile: async (profile: Profile) => {
        return pubApiClient.post('/auth/create-profile', profile);
    },

    getProfile: async (userId: string) => {
        return apiClient.get<ProfileResponse>('/auth/get-profile', { user_id: userId });
    },

    updateProfile: async (profile: UpdateProfile) => {
        return apiClient.post('/auth/update-profile', profile);
    },
};
"""
