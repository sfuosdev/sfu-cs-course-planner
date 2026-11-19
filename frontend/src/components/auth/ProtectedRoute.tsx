import { Navigate, Outlet } from "react-router";
import { useAuth } from "#contexts/AuthContext";

export const ProtectedRoute = () => {
  const { currentUser, isLoading } = useAuth();
  if (isLoading) {
    return <div>Loading...</div>;
  }
  if (!currentUser) {
    return <Navigate to="/login" replace />;
  }
  return <Outlet />;
};
