import type { Course } from '../../types/Course'
import { terms } from './constants'
import type { SemesterCourses, SemesterOption, Term } from './types'

export const termKey = (year: number, term: Term) =>
  `year-${year}-${term.toLowerCase()}`

export const formatTermLabel = (key: string) => {
  const [, year, term] = key.split('-')
  return `Year ${year} · ${term[0].toUpperCase()}${term.slice(1)}`
}

export const getTotalUnits = (courses: Course[]) =>
  courses.reduce((total, course) => total + course.credits, 0)

export const getPlannedCoursesCount = (plannedCourses: SemesterCourses) =>
  Object.values(plannedCourses).flat().length

export const getPlannedUnits = (plannedCourses: SemesterCourses) =>
  getTotalUnits(Object.values(plannedCourses).flat())

export const getSemesterOptions = (years: number[]): SemesterOption[] =>
  years.flatMap((year) =>
    terms.map((term) => {
      const key = termKey(year, term)
      return { key, label: formatTermLabel(key) }
    }),
  )

export const isCoursePlanned = (
  plannedCourses: SemesterCourses,
  courseId: number,
) =>
  Object.values(plannedCourses)
    .flat()
    .some((course) => course.id === courseId)
