import type { Course } from './Course'

export type Season = 'fall' | 'spring' | 'summer'

export interface PlanCourse {
    id: number
    course: Course
    year: number
    season: Season
}

export interface Plan {
    id: number
    name: string
    planCourses: PlanCourse[]
}
