import type { Plan, PlanCourse, Season } from '#types/Plan'
import { ApiError, apiRequest } from './apiClient'

export async function loadOrCreatePlan(signal: AbortSignal): Promise<Plan> {
    const plans = await apiRequest<{ id: number}[]>(`/plans`, { signal})
    return plans.length > 0
    ? apiRequest<Plan>(`/plans/${plans[0].id}`, { signal })
    : apiRequest<Plan>('/plans', { method: 'POST', body: JSON.stringify({ name: 'My plan' }) })
}

export const addPlanCourse = (planId: number, courseId: number, year: number, season: Season) =>
    apiRequest<PlanCourse>(`/plans/${planId}/courses`, {
        method: 'POST',
        body: JSON.stringify({ courseId, year, season})
    })

export async function loadPlanOrGuest(signal: AbortSignal): Promise<Plan | null> {
  try {
    return await loadOrCreatePlan(signal)
  } catch (err) {
    if (err instanceof ApiError && err.status === 401) return null
    throw err
  }
}

export const movePlanCourse = (planId: number, planCourseId: number, year: number, season: Season) =>
  apiRequest<PlanCourse>(`/plans/${planId}/courses/${planCourseId}`, {
    method: 'PATCH',
    body: JSON.stringify({ year, season }),
  })

export const removePlanCourse = (planId: number, planCourseId: number) =>
  apiRequest<void>(`/plans/${planId}/courses/${planCourseId}`, { method: 'DELETE' })