import type { Course } from "../../../types/course";
import styles from "./CourseSearchCard.module.css";
interface CourseSearchCardProps {
  course: Course;
  onSelect: (course: Course) => void;
}

export const CourseSearchCard = ({
  course,
  onSelect,
}: CourseSearchCardProps) => {
  return (
    <div className={styles.card}>
      <h3 className={styles.code}>{course.courseCode}</h3>
      <p className={styles.title}>{course.title}</p>
      <p className={styles.credits}>({course.credits})</p>
      <button
        type="button"
        className={styles.button}
        onClick={() => {
          onSelect(course);
        }}
      >
        Add course
      </button>
    </div>
  );
};
