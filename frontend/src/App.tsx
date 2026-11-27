import { useState } from "react";
import "./App.css";
import { Route, Routes, useNavigate } from "react-router";
import { GuestRoute } from "./components/auth/GuestRoute";
import { ProtectedRoute } from "./components/auth/ProtectedRoute";
import { Planner } from "./components/planner/Planner";
import {
  formatTermLabel,
  getPlannedCoursesCount,
  getPlannedUnits,
  termKey,
} from "./components/planner/plannerUtils";
import { ProgressRail } from "./components/ProgressRail";
import { SearchPanel } from "./components/SearchPanel";
import { useAuth } from "#contexts/AuthContext";
import type { Course } from "#types/Course";
import { Login } from "./pages/Login";
import { Placeholder } from "./pages/Placeholder";
import { SignUp } from "./pages/SignUp";
import { usePlan} from "#services/hooks/usePlan";

function Dashboard() {
  const [activeConcentration, setActiveConcentration] = useState(
    "Artificial Intelligence",
  );
  const [years, setYears] = useState([1, 2, 3, 4]);
  const [selectedTerm, setSelectedTerm] = useState(termKey(1, "Fall"));
  const { plannedCourses, isCoursePlanned, addCourse, removeCourse, moveCourse, status } = usePlan();
  const [plannerMessage, setPlannerMessage] = useState<string | null>(null);
  const navigate = useNavigate();
  const { currentUser, clearCurrentUser } = useAuth();

  const handleSelectCourse = (course: Course) => {
    if (isCoursePlanned(course.id)) {
      setPlannerMessage(`${course.courseCode} is already in your plan.`);
      return;
    }

    addCourse(course, selectedTerm);
    setPlannerMessage(
      `${course.courseCode} was added to ${formatTermLabel(selectedTerm)}.`,
    );
  };

  const handleMoveCourse = (fromTerm: string, toTerm: string, courseId: number) => {
        if (!toTerm || fromTerm === toTerm) return;
        moveCourse(fromTerm, toTerm, courseId);
    };

  const handleLogout = async () => {
    try {
      // TODO: Properly connect to API
      // await logoutUser();
    } catch (error) {
      console.error("Error logging out", error);
    } finally {
      clearCurrentUser();
    }
  };

  return (
    <main className="app-shell">
      <header className="topbar">
        <a
          className="brand"
          href="#planner"
          aria-label="SFU CS Course Planner home"
        >
          <span className="brand-mark" aria-hidden="true">
            C
          </span>
          <span className="brand-copy">
            <span className="brand-name">Course Planner</span>
            <span className="brand-school">SFU Computing Science</span>
          </span>
        </a>
        <div className="topbar-actions">
          <span className="save-state">
            <span aria-hidden="true" />
            {status}
            {currentUser ? (
              <button type="button" onClick={handleLogout}>
                Log out
              </button>
            ) : (
              <button type="button" onClick={() => navigate("/login")}>
                Log in
              </button>
            )}
            <section id="temp-user-details">
              {currentUser
                ? `${currentUser.username} | ${currentUser.email}`
                : "Guest"}
            </section>
          </span>
        </div>
      </header>

      <div className="workspace">
        <ProgressRail plannedUnits={getPlannedUnits(plannedCourses)} />
        <Planner
          activeConcentration={activeConcentration}
          years={years}
          selectedTerm={selectedTerm}
          plannedCourses={plannedCourses}
          message={plannerMessage}
          onSelectConcentration={setActiveConcentration}
          onSelectTerm={setSelectedTerm}
          onAddYear={() => setYears((current) => [...current, current.length + 1])}
          onMoveCourse={handleMoveCourse}
          onRemoveCourse={removeCourse}
        />
        <SearchPanel
          selectedTerm={selectedTerm}
          plannedCoursesCount={getPlannedCoursesCount(plannedCourses)}
          onSelectCourse={handleSelectCourse}
        />
      </div>
    </main>
  );
}

function App() {
  return (
    <Routes>
      <Route path="/" element={<Dashboard />} />

      <Route element={<GuestRoute />}>
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<SignUp />} />
      </Route>

      <Route element={<ProtectedRoute />}>
        <Route path="/placeholder" element={<Placeholder />} />
      </Route>
    </Routes>
  );
}

export default App;
