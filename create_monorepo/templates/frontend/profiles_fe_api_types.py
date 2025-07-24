PROFILES_FE_API_TYPES = """export interface Profile {
    user_id: string;
    email: string;
    first_name?: string;
    last_name?: string;
}

export interface ProfileResponse {
    status: string;
    first_name?: string;
    last_name?: string;
}

export interface UpdateProfile {
    user_id: string;
    email?: string;
    first_name?: string;
    last_name?: string;
}
"""
