export class ApiError extends Error {
    status: number
    constructor(message: string, status: number) {
        super(message)
        this.status = status
    }
}

export async function apiRequest<T>(path: string, init: RequestInit = {}): Promise<T> {
    let response: Response
    try {
        response = await fetch(`/api${path}`, {
            ...init,
            headers: { 'Content-Type': 'application/json', ...init.headers },
        })
    } catch (err) {
        if (init.signal?.aborted)
            throw err
        throw new ApiError("Can't reach the server. Check your connection and try again.", 0)
    }

    if (!response.ok) {
        const data= await response.json().catch(() => null)
        const message = typeof data?.detail === 'string' ? data.detail : `Request failed (${response.status})`
        throw new ApiError(message, response.status)
    }

    return response.status === 204 ? (undefined as T) : response.json()
}