import { useEffect, useState, type ReactNode } from "react";
import { MOCK_COURSES } from "#mock-data/MockCourses";
import { simulateNetworkDelay } from "#utils/utils";
import { CourseContext } from "./CourseContext";
import type { Course } from "#types/Course";

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
        console.error(error);
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
