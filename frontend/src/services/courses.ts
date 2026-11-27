import type { Course, CourseDetails } from '#types/Course'
import { apiRequest } from './apiClient'

export const searchCourses = (q: string, signal: AbortSignal) =>
    apiRequest<Course[]>(`/courses?${new URLSearchParams({q, limit: '25'})}`, {signal})

export const getCourseDetails = (courseCode: string, signal: AbortSignal) =>
    apiRequest<CourseDetails>(`/courses/${encodeURIComponent(courseCode)}`, {signal})

export const getAllCourses = () => apiRequest<Course[]>('/courses')