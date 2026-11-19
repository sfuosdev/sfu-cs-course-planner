import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.tsx";
import { BrowserRouter } from "react-router";
import { AuthContextProvider } from "./contexts/AuthContextProvider.tsx";
import { CourseContextProvider } from "./contexts/CourseContextProvider.tsx";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <BrowserRouter>
      <AuthContextProvider>
        <CourseContextProvider>
          <App />
        </CourseContextProvider>
      </AuthContextProvider>
    </BrowserRouter>
  </StrictMode>,
);
