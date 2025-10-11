import { useContext } from "react";
import { Navigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

const ProtectedRoute = ({ children, allowedRoles }) => {
  const { token, role, loading } = useContext(AuthContext);

  if (loading) return <p>Loading...</p>; // wait for AuthContext to finish

  // redirect if not logged in or role is not allowed
  if (!token || !role || (allowedRoles && !allowedRoles.includes(role))) {
    return <Navigate to="/" />;
  }

  return children;
};

export default ProtectedRoute;
