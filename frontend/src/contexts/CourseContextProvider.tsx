import { useEffect, useState, type ReactNode } from "react";

import { getAllCourses } from "#services/courses";
import { CourseContext } from "./CourseContext";
import type { Course } from "#types/Course";
import { getErrorMessage } from "#services/errors";

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
        setAllCourses(await getAllCourses());
      } catch (error) {
        setError(getErrorMessage(error));
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
