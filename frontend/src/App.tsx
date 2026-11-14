import { useState } from 'react'
import './App.css'
import { CourseSearch } from './components/CourseSearch/CourseSearch'
import { CourseContextProvider } from './contexts/CourseContext'
import type { Course } from './types/course'

const concentrations = [
  'Artificial Intelligence',
  'Visual & Interactive Computing',
  'Computing Systems',
  'Information Systems',
  'Programming Languages & Software',
  'Theoretical Computing Science',
]
const terms = ['Fall', 'Spring', 'Summer']
const termKey = (year: number, term: string) => `year-${year}-${term.toLowerCase()}`
const formatTermLabel = (key: string) => {
  const [, year, term] = key.split('-')
  return `Year ${year} · ${term[0].toUpperCase()}${term.slice(1)}`
}

function Dashboard() {
  const [activeConcentration, setActiveConcentration] = useState(concentrations[0])
  const [years, setYears] = useState([1, 2, 3, 4])
  const [selectedTerm, setSelectedTerm] = useState(termKey(1, 'Fall'))
  const [plannedCourses, setPlannedCourses] = useState<Record<string, Course[]>>({})

  const plannedUnits = Object.values(plannedCourses)
    .flat()
    .reduce((total, course) => total + course.credits, 0)

  const handleSelectCourse = (course: Course) => {
    setPlannedCourses((current) => {
      const currentTermCourses = current[selectedTerm] ?? []
      if (currentTermCourses.some((planned) => planned.id === course.id)) return current
      return { ...current, [selectedTerm]: [...currentTermCourses, course] }
    })
  }

  return (
    <main className="app-shell">
      <header className="topbar">
        <a className="brand" href="#planner" aria-label="SFU CS Course Planner home">
          <span className="brand-mark" aria-hidden="true">C</span>
          <span className="brand-copy">
            <span className="brand-name">Course Planner</span>
            <span className="brand-school">SFU Computing Science</span>
          </span>
        </a>
        <div className="topbar-actions">
          <span className="save-state"><span aria-hidden="true" />Draft plan</span>
        </div>
      </header>

      <div className="workspace">
        <aside className="progress-rail" aria-labelledby="progress-heading">
          <div className="rail-heading">
            <p className="section-kicker">Your degree</p>
            <h1 id="progress-heading">Progress</h1>
            <p className="rail-description">A snapshot of your path to graduation.</p>
          </div>
          <section className="degree-card" aria-label="Degree progress summary">
            <div className="degree-card-top">
              <span className="degree-icon" aria-hidden="true">✦</span>
              <span className="degree-label">Computing Science</span>
            </div>
            <div className="credit-count"><strong>{plannedUnits}</strong><span>units planned</span></div>
            <div className="progress-track" role="progressbar" aria-label="Degree units planned" aria-valuenow={Math.min(plannedUnits, 120)} aria-valuemin={0} aria-valuemax={120}>
              <span style={{ width: `${Math.min((plannedUnits / 120) * 100, 100)}%` }} />
            </div>
            <p className="degree-footnote">Add courses to see your progress here.</p>
          </section>

          <section className="requirements" aria-labelledby="requirements-heading">
            <div className="section-title-row">
              <h2 id="requirements-heading">Requirement groups</h2>
              <button className="text-button" type="button" aria-label="View all degree requirements">View all</button>
            </div>
            <div className="requirement-row"><span className="requirement-icon breadth" aria-hidden="true">◈</span><span className="requirement-copy"><strong>Lower division</strong><small>Core foundations</small></span><span className="requirement-count">To track</span></div>
            <div className="requirement-row"><span className="requirement-icon depth" aria-hidden="true">⌘</span><span className="requirement-copy"><strong>Upper division</strong><small>Advanced courses</small></span><span className="requirement-count">To track</span></div>
            <div className="requirement-row"><span className="requirement-icon electives" aria-hidden="true">✳</span><span className="requirement-copy"><strong>Electives</strong><small>Explore your interests</small></span><span className="requirement-count">To track</span></div>
          </section>
          <div className="rail-tip"><span className="tip-icon" aria-hidden="true">✦</span><p><strong>Make it yours</strong><br />Build a plan that fits your goals and pace.</p></div>
          <p className="requirements-note">Requirements can vary by calendar year. Always confirm with the SFU Calendar.</p>
        </aside>

        <section className="planner" id="planner" aria-labelledby="planner-heading">
          <div className="planner-heading-row">
            <div><p className="section-kicker">Your academic journey</p><h2 id="planner-heading">My course plan</h2></div>
            <span className="term-button"><span aria-hidden="true">▦</span> Fall 2026 <span className="chevron" aria-hidden="true">⌄</span></span>
          </div>
          <nav className="concentration-nav" aria-label="Browse concentrations">
            {concentrations.map((concentration) => (
              <button className={`concentration-tab${activeConcentration === concentration ? ' active' : ''}`} type="button" aria-pressed={activeConcentration === concentration} onClick={() => setActiveConcentration(concentration)} key={concentration}>{concentration}</button>
            ))}
          </nav>
          <div className="planner-caption"><span>Select a term, then add matching courses from search.</span><span className="legend-button"><span aria-hidden="true">ⓘ</span> Click a term to choose it</span></div>

          <div className="year-list">
            {years.map((year) => (
              <section className="year-section" aria-labelledby={`year-${year}`} key={year}>
                <div className="year-label"><span id={`year-${year}`}>Year {year}</span><span className="year-rule" /></div>
                <div className="term-grid">
                  {terms.map((term) => {
                    const key = termKey(year, term)
                    const courses = plannedCourses[key] ?? []
                    const units = courses.reduce((sum, course) => sum + course.credits, 0)
                    return (
                      <div className={`term-card${selectedTerm === key ? ' selected' : ''}`} key={term} role="button" tabIndex={0} aria-pressed={selectedTerm === key} onClick={() => setSelectedTerm(key)} onKeyDown={(event) => {
                        if (event.key === 'Enter' || event.key === ' ') {
                          event.preventDefault()
                          setSelectedTerm(key)
                        }
                      }}>
                        <div className="term-card-heading"><h3>{term}</h3><span>{term === 'Fall' ? 'Sep – Dec' : term === 'Spring' ? 'Jan – Apr' : 'May – Aug'}</span></div>
                        <div className="term-dropzone">
                          {courses.length === 0 ? <><span className="plus-mark" aria-hidden="true">+</span><span>{selectedTerm === key ? 'Selected for courses' : 'Choose term'}</span></> : courses.map((course) => <span className="planned-course" key={course.id}>{course.courseCode}</span>)}
                        </div>
                        <div className="term-units">{units} units</div>
                      </div>
                    )
                  })}
                </div>
              </section>
            ))}
          </div>
          <button className="add-year-button" type="button" onClick={() => setYears((currentYears) => [...currentYears, currentYears.length + 1])}><span aria-hidden="true">+</span> Add another year</button>
        </section>

        <aside className="search-panel" aria-labelledby="search-heading">
          <div className="search-panel-heading">
            <div><p className="section-kicker">Build your plan</p><h2 id="search-heading">Find a course</h2></div>
            <span className="search-count">{Object.values(plannedCourses).flat().length} added</span>
          </div>
          <p className="search-target">Adding to {formatTermLabel(selectedTerm)}</p>
          <CourseSearch onSelect={handleSelectCourse} />
          <div className="search-panel-footer"><span className="footer-sparkle" aria-hidden="true">✦</span><p>Choose a term, then use Add course in a search result.</p></div>
        </aside>
      </div>
    </main>
  )
}

function App() {
  return <CourseContextProvider><Dashboard /></CourseContextProvider>
}

export default App
