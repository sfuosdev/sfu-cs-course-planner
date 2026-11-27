import { useState } from 'react'
import { useAuth } from '#contexts/AuthContext'
import { getErrorMessage } from '#services/errors'
import { addPlanCourse, loadPlanOrGuest, movePlanCourse, removePlanCourse } from '#services/plans'
import type { Course } from '#types/Course'
import type { PlanCourse, Season } from '#types/Plan'
import { useRequest } from './useRequest'

// "year-2-fall" <-> { year: 2, season: "fall" }, the key format the planner already uses
const parseTermKey = (key: string) => {
  const [, year, season] = key.split('-')
  return { year: Number(year), season: season as Season }
}
const toTermKey = (pc: PlanCourse) => `year-${pc.year}-${pc.season}`

export function usePlan() {
  const { currentUser } = useAuth()
  // The key changes on login/logout, so the plan reloads automatically
  const { data: plan, error: loadError, setData } = useRequest(
    `plan-${currentUser?.email ?? 'guest'}`,
    loadPlanOrGuest,
  )
  const [guestCourses, setGuestCourses] = useState<PlanCourse[]>([])
  const [saveError, setSaveError] = useState<string>()

  const isGuest = plan === null
  const planCourses = isGuest ? guestCourses : plan?.planCourses ?? []

  // Same shape App/Planner already use: { "year-1-fall": Course[] }
  const plannedCourses: Record<string, Course[]> = {}
  for (const pc of planCourses) (plannedCourses[toTermKey(pc)] ??= []).push(pc.course)

  const findPlanCourse = (courseId: number) => planCourses.find((pc) => pc.course.id === courseId)
  const setPlanCourses = (update: (cs: PlanCourse[]) => PlanCourse[]) =>
    isGuest ? setGuestCourses(update) : setData((p) => p && { ...p, planCourses: update(p.planCourses) })

  // planId is null for guests: the change stays local and nothing is sent to the server
  const run = async (action: (planId: number | null) => Promise<void>) => {
    if (plan === undefined) return // still loading
    try {
      await action(plan?.id ?? null)
      setSaveError(undefined)
    } catch (err) {
      setSaveError(getErrorMessage(err))
    }
  }

  const addCourse = (course: Course, termKey: string) =>
    run(async (planId) => {
      if (findPlanCourse(course.id)) return
      const { year, season } = parseTermKey(termKey)
      const created = planId === null
        ? { id: -Date.now(), course, year, season }
        : await addPlanCourse(planId, course.id, year, season)
      setPlanCourses((cs) => [...cs, created])
    })

  const removeCourse = (_termKey: string, courseId: number) =>
    run(async (planId) => {
      const pc = findPlanCourse(courseId)
      if (!pc) return
      if (planId !== null) await removePlanCourse(planId, pc.id)
      setPlanCourses((cs) => cs.filter((c) => c.id !== pc.id))
    })

  const moveCourse = (_fromTerm: string, toTerm: string, courseId: number) =>
    run(async (planId) => {
      const pc = findPlanCourse(courseId)
      if (!pc) return
      const { year, season } = parseTermKey(toTerm)
      const moved = planId === null ? { ...pc, year, season } : await movePlanCourse(planId, pc.id, year, season)
      setPlanCourses((cs) => cs.map((c) => (c.id === pc.id ? moved : c)))
    })

  const status = isGuest ? 'Guest · sign in to save' : loadError ?? saveError ?? (plan ? 'Saved' : 'Loading…')

  return { plannedCourses, isCoursePlanned: (id: number) => !!findPlanCourse(id), addCourse, removeCourse, moveCourse, status }
}