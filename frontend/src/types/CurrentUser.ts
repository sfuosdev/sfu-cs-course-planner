export interface CurrentUser {
  userId: string;
  email: string;
  username: string;
}

export interface CurrentUserResponse {
  user: CurrentUser;
}
