import { useContext } from "react";
import { createContext } from "react";
import type { CurrentUser } from "#types/CurrentUser";

interface AuthContextType {
  currentUser: CurrentUser | null;
  isLoading: boolean;
  refreshCurrentUser: () => Promise<void>;
  clearCurrentUser: () => void;
}

export const AuthContext = createContext<AuthContextType | undefined>(
  undefined,
);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("Error with useAuth hook.");
  }
  return context;
};
