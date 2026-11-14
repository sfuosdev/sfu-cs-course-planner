import { useState } from "react";
import { useCourses } from "../../contexts/CourseContext";
import type { Course } from "../../types/course";
import { CourseSearchCard } from "./CourseSearchCard/CourseSearchCard";
import styles from "./CourseSearch.module.css";

interface CourseSearchProps {
  onSelect: (course: Course) => void;
}

export const CourseSearch = ({ onSelect }: CourseSearchProps) => {
  const { allCourses, isLoading, error } = useCourses();
  const [searchQuery, setSearchQuery] = useState<string>("");

  if (isLoading) {
    return (
      <section className={styles.container}>
        <input className={styles.input} disabled placeholder="Loading..." />
      </section>
    );
  }
  if (error) {
    return (
      <section className={styles.container}>
        <div className={styles.message}>{error}</div>
      </section>
    );
  }

  const normalizedSearchQuery = searchQuery.trim().toLowerCase();
  const filteredCourses =
    normalizedSearchQuery === ""
      ? []
      : allCourses.filter((course) => {
          const courseCode = course.courseCode.trim().toLowerCase();
          const courseTitle = course.title.trim().toLowerCase();
          return (
            courseCode.includes(normalizedSearchQuery) ||
            courseTitle.includes(normalizedSearchQuery)
          );
        });

  return (
    <section className={styles.container}>
      <form
        onSubmit={(e) => {
          e.preventDefault();
        }}
      >
        <input
          type="searchQuery"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search courses..."
          className={styles.input}
        />
      </form>

      {normalizedSearchQuery === "" ? (
        <p className={styles.message}>Start typing to search.</p>
      ) : filteredCourses.length === 0 ? (
        <p className={styles.message}>No courses match the search.</p>
      ) : (
        <div className={styles.results}>
          {filteredCourses.map((course) => {
            return (
              <CourseSearchCard
                key={course.id}
                course={course}
                onSelect={onSelect}
              />
            );
          })}
        </div>
      )}
    </section>
  );
};
