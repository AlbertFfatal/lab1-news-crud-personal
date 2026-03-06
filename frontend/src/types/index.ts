export interface UserRegister {
  name: string;
  email: string;
  password: string;
  is_author_verified?: boolean;
  is_admin?: boolean;
  avatar?: string | null;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}
export interface NewsCreate {
  title: string;
  content: Record<string, any>;
  cover?: string;
}

export interface News {
  id: number;
  title: string;
  content: Record<string, any>;
  publication_date: string;
  author_id: number;
  cover?: string;
}