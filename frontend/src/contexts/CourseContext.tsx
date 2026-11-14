import { useContext, useEffect, useState, type ReactNode } from "react";
import type { Course } from "../types/course";
import { MOCK_COURSES } from "../mock-data/courses";
import { createContext } from "react";
import { simulateNetworkDelay } from "../utils/utils";

interface CourseContext {
  allCourses: Course[];
  isLoading: boolean;
  error: string | null;
}

const CourseContext = createContext<CourseContext | undefined>(undefined);

export const CourseContextProvider = ({
  children,
}: {
  children: ReactNode;
}) => {
  const [allCourses, setAllCourses] = useState<Course[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchCourses = async () => {
      try {
        setIsLoading(true);

        // Simulating network delay for 1 second (1000ms)
        await simulateNetworkDelay(1000);

        setAllCourses(MOCK_COURSES);
      } catch (error) {
        setError("Error when fetching courses.");
      } finally {
        setIsLoading(false);
      }
    };
    fetchCourses();
  }, []);

  return (
    <CourseContext.Provider value={{ allCourses, isLoading, error }}>
      {children}
    </CourseContext.Provider>
  );
};

export const useCourses = () => {
  const context = useContext(CourseContext);
  if (!context) {
    throw new Error("Error with useCourses hook.");
  }
  return context;
};
