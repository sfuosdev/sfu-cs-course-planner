import { useContext } from "react";
import type { Course } from "#types/Course";
import { createContext } from "react";

interface CourseContext {
  allCourses: Course[];
  isLoading: boolean;
  error: string | null;
}

export const CourseContext = createContext<CourseContext | undefined>(
  undefined,
);

export const useCourses = () => {
  const context = useContext(CourseContext);
  if (!context) {
    throw new Error("Error with useCourses hook.");
  }
  return context;
};
