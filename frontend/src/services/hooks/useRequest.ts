import { useEffect, useState } from 'react'
import { getErrorMessage } from '../errors'

export function useRequest<T>(key: string | null, request: (signal: AbortSignal) => Promise<T>) {
    const [state, setState] = useState<{ data?: T; error?: string; isLoading: boolean }>({ isLoading: false })
    const [attempt, setAttempt] = useState(0)

    useEffect(() => {
        if (key === null) return setState({ isLoading: false })
        const controller = new AbortController()
        setState((s) => ({ ...s, isLoading: true, error: undefined }))
        request(controller.signal)
            .then((data) => setState({ data, isLoading: false }))
            .catch((err) => {
                if (!controller.signal.aborted) setState({ error: getErrorMessage(err), isLoading: false })
            })
        return () => controller.abort() // cancels stale requests; also stops StrictMode from creating 2 plans
    }, [key, attempt])

    const setData = (update: (data: T) => T) =>
        setState((s) => (s.data === undefined ? s : { ...s, data: update(s.data) }))

    return { ...state, setData, retry: () => setAttempt((a) => a + 1) }
}