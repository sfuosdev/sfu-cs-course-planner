import type { Course } from '../../types/Course'
import { termDates } from './constants'
import { getTotalUnits } from './plannerUtils'
import type { SemesterOption, Term } from './types'

type TermCardProps = {
  term: Term
  semesterKey: string
  courses: Course[]
  isSelected: boolean
  semesterOptions: SemesterOption[]
  onSelect: (semesterKey: string) => void
  onMoveCourse: (fromTerm: string, toTerm: string, courseId: number) => void
  onRemoveCourse: (semesterKey: string, courseId: number) => void
}

export function TermCard({
  term,
  semesterKey,
  courses,
  isSelected,
  semesterOptions,
  onSelect,
  onMoveCourse,
  onRemoveCourse,
}: TermCardProps) {
  const units = getTotalUnits(courses)

  return (
    <section
      className={`term-card${isSelected ? ' selected' : ''}`}
      onClick={(event) => {
        if (
          event.target instanceof HTMLElement &&
          event.target.closest('button, select')
        ) {
          return
        }
        onSelect(semesterKey)
      }}
    >
      <div className="term-card-heading">
        <button
          type="button"
          className="term-select-button"
          aria-pressed={isSelected}
          onClick={() => onSelect(semesterKey)}
        >
          <span>{term}</span>
          <span>{termDates[term]}</span>
        </button>
      </div>

      <div className="term-dropzone">
        {courses.length === 0 ? (
          <>
            <span className="plus-mark" aria-hidden="true">+</span>
            <span>{isSelected ? 'Selected for courses' : 'Choose term'}</span>
          </>
        ) : (
          courses.map((course) => (
            <div className="planned-course" key={course.id}>
              <span>{course.courseCode}</span>
              <select
                className="move-course-select"
                defaultValue=""
                aria-label={`Move ${course.courseCode} from ${term}`}
                onChange={(event) =>
                  onMoveCourse(semesterKey, event.target.value, course.id)
                }
              >
                <option value="" disabled>
                  Move to…
                </option>
                {semesterOptions
                  .filter((semester) => semester.key !== semesterKey)
                  .map((semester) => (
                    <option key={semester.key} value={semester.key}>
                      {semester.label}
                    </option>
                  ))}
              </select>
              <button
                type="button"
                className="remove-course-button"
                aria-label={`Remove ${course.courseCode} from ${term}`}
                onClick={() => onRemoveCourse(semesterKey, course.id)}
              >
                ×
              </button>
            </div>
          ))
        )}
      </div>

      <div className="term-units">{units} units</div>
    </section>
  )
}
