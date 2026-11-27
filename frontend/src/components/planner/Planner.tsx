import { concentrations, terms } from './constants'
import { getSemesterOptions, termKey } from './plannerUtils'
import { TermCard } from './TermCard'
import type { SemesterCourses } from './types'

type PlannerProps = {
  activeConcentration: string
  years: number[]
  selectedTerm: string
  plannedCourses: SemesterCourses
  message: string | null
  onSelectConcentration: (concentration: string) => void
  onSelectTerm: (semesterKey: string) => void
  onAddYear: () => void
  onMoveCourse: (fromTerm: string, toTerm: string, courseId: number) => void
  onRemoveCourse: (semesterKey: string, courseId: number) => void
}

export function Planner({
  activeConcentration,
  years,
  selectedTerm,
  plannedCourses,
  message,
  onSelectConcentration,
  onSelectTerm,
  onAddYear,
  onMoveCourse,
  onRemoveCourse,
}: PlannerProps) {
  const semesterOptions = getSemesterOptions(years)

  return (
    <section className="planner" id="planner" aria-labelledby="planner-heading">
      <div className="planner-heading-row">
        <div>
          <p className="section-kicker">Your academic journey</p>
          <h2 id="planner-heading">My course plan</h2>
        </div>
        <span className="term-button">
          <span aria-hidden="true">▦</span>
          Fall 2026
          <span className="chevron" aria-hidden="true">⌄</span>
        </span>
      </div>

      <nav className="concentration-nav" aria-label="Browse concentrations">
        {concentrations.map((concentration) => (
          <button
            className={`concentration-tab${activeConcentration === concentration ? ' active' : ''}`}
            type="button"
            aria-pressed={activeConcentration === concentration}
            onClick={() => onSelectConcentration(concentration)}
            key={concentration}
          >
            {concentration}
          </button>
        ))}
      </nav>

      <div className="planner-caption">
        <span>Select a term, then add matching courses from search.</span>
        <span className="legend-button">
          <span aria-hidden="true">ⓘ</span> Click a term to choose it
        </span>
      </div>

      {message && (
        <p className="planner-message" aria-live="polite">
          {message}
        </p>
      )}

      <div className="year-list">
        {years.map((year) => (
          <section className="year-section" aria-labelledby={`year-${year}`} key={year}>
            <div className="year-label">
              <span id={`year-${year}`}>Year {year}</span>
              <span className="year-rule" />
            </div>
            <div className="term-grid">
              {terms.map((term) => {
                const semesterKey = termKey(year, term)

                return (
                  <TermCard
                    key={term}
                    term={term}
                    semesterKey={semesterKey}
                    courses={plannedCourses[semesterKey] ?? []}
                    isSelected={selectedTerm === semesterKey}
                    semesterOptions={semesterOptions}
                    onSelect={onSelectTerm}
                    onMoveCourse={onMoveCourse}
                    onRemoveCourse={onRemoveCourse}
                  />
                )
              })}
            </div>
          </section>
        ))}
      </div>

      <button className="add-year-button" type="button" onClick={onAddYear}>
        <span aria-hidden="true">+</span> Add another year
      </button>
    </section>
  )
}
