export interface LoginRequest {
  email: string;
  password: string;
}

export interface SignUpRequest {
  email: string;
  password: string;
  username: string;
}

export interface AuthErrorResponse {
  error: string;
}
