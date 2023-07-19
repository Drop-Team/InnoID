export interface User {
  user_id: string;
  email: string;
}

export interface Tokens {
  access_token: string;
  refresh_token: string;
}

export interface LoginContext {}
