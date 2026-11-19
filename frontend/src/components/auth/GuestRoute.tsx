import { Navigate, Outlet } from "react-router";
import { useAuth } from "#contexts/AuthContext";

export const GuestRoute = () => {
  const { currentUser, isLoading } = useAuth();
  if (isLoading) {
    return <div>Loading...</div>;
  }
  if (currentUser) {
    return <Navigate to="/" replace />;
  }
  return <Outlet />;
};
