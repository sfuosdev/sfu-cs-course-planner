import { useState, type SyntheticEvent } from "react";
import { useNavigate } from "react-router";
import { cleanString } from "#utils/strings";
import { loginUser } from "#api/AuthApi";
import { useAuth } from "#contexts/AuthContext";

export const Login = () => {
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [error, setError] = useState<string>("");
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [showPassword, setShowPassword] = useState<boolean>(false);
  const navigate = useNavigate();
  const { refreshCurrentUser } = useAuth();

  const handleSubmit = async (e: SyntheticEvent) => {
    e.preventDefault();
    setError("");
    const cleanEmail = cleanString(email);

    if (cleanEmail === "" || password === "") {
      setError("Please enter email and password.");
      return;
    }

    setIsSubmitting(true);
    try {
      await loginUser({ email: cleanEmail, password });
      await refreshCurrentUser();

      // TODO: Temporarily navigates to placeholder, replace with actual page later
      navigate("/placeholder");
    } catch (error) {
      setError("Error logging in");
      console.error(error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <>
      {error !== "" && <div>{error}</div>}
      <form onSubmit={handleSubmit}>
        <label htmlFor="email-input">Email</label>
        <input
          id="email-input"
          type="email"
          placeholder="user@example.com..."
          value={email}
          onChange={(e) => {
            setEmail(e.target.value);
          }}
          required
          autoComplete="email"
        />

        <label htmlFor="password-input">Password</label>
        <input
          id="password-input"
          type={showPassword ? "text" : "password"}
          placeholder="Enter your password..."
          value={password}
          onChange={(e) => {
            setPassword(e.target.value);
          }}
          required
          autoComplete="current-password"
        />
        <button
          type="button"
          onClick={() => {
            setShowPassword(!showPassword);
          }}
        >
          {showPassword ? "Hide" : "Show"}
        </button>

        <button type="submit" disabled={isSubmitting}>
          {isSubmitting ? "Logging in..." : "Log in"}
        </button>
      </form>
    </>
  );
};
