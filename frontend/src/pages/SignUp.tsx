import { signUpUser } from "#api/AuthApi";
import { cleanString } from "#utils/strings";
import { useState, type SyntheticEvent } from "react";
import { useNavigate } from "react-router";

export const SignUp = () => {
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [confirmPassword, setConfirmPassword] = useState<string>("");
  const [username, setUsername] = useState<string>("");
  const [error, setError] = useState<string>("");
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [showPassword, setShowPassword] = useState<boolean>(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: SyntheticEvent) => {
    e.preventDefault();
    setError("");
    const cleanEmail = cleanString(email);
    const cleanUsername = cleanString(username);

    if (cleanEmail === "" || password === "" || cleanUsername === "") {
      setError("Please enter email, username, and password.");
      return;
    }

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    setIsSubmitting(true);
    try {
      await signUpUser({
        email: cleanEmail,
        password,
        username: cleanUsername,
      });

      // TODO: Temporarily navigates to login, replace with actual page later
      navigate("/login");
    } catch (error) {
      setError("Error signing up");
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

        <label htmlFor="username-input">Username</label>
        <input
          id="username-input"
          type="text"
          placeholder="Enter your username..."
          value={username}
          onChange={(e) => {
            setUsername(e.target.value);
          }}
          required
          autoComplete="username"
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
        />

        <label htmlFor="password-input">Confirm password</label>
        <input
          id="confirm-password-input"
          type={showPassword ? "text" : "password"}
          placeholder="Confirm your password..."
          value={confirmPassword}
          onChange={(e) => {
            setConfirmPassword(e.target.value);
          }}
          required
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
          {isSubmitting ? "Creating account..." : "Sign up"}
        </button>
      </form>
    </>
  );
};
