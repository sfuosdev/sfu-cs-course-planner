import { useCallback, useEffect, useState, type ReactNode } from "react";
import type { CurrentUser } from "#types/CurrentUser";
import { requestCurrentUser } from "#api/AuthApi";
import { AuthContext } from "./AuthContext";

export const AuthContextProvider = ({ children }: { children: ReactNode }) => {
  const [currentUser, setCurrentUser] = useState<CurrentUser | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  const refreshCurrentUser = useCallback(async (): Promise<void> => {
    setIsLoading(true);
    try {
      const user = await requestCurrentUser();
      setCurrentUser(user);
    } catch (error) {
      setCurrentUser(null);
      console.error(`Failed to load current user: ${error}`);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const clearCurrentUser = useCallback(() => {
    setCurrentUser(null);
  }, []);

  useEffect(() => {
    const loadInitialUser = async (): Promise<void> => {
      await refreshCurrentUser();
    };
    loadInitialUser();
  }, [refreshCurrentUser]);

  return (
    <AuthContext.Provider
      value={{
        currentUser,
        isLoading,
        refreshCurrentUser,
        clearCurrentUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};
