import { ApiError } from "./apiClient";

export function getErrorMessage(err: unknown): string {
    if (!(err instanceof ApiError)) return 'Something went wrong. Please try again.'
    if (err.status === 401) return 'Please sign in to save your plan.'
    if (err.status >= 500) return 'Server error. Please try again shortly.'
    return err.message
}