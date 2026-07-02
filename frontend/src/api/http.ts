export const BASE_URL = import.meta.env.VITE_API_BASE_URL

type RefreshHandler = () => Promise<boolean>

let refreshHandler: RefreshHandler | null = null

export function setRefreshHandler(handler: RefreshHandler) {
    refreshHandler = handler
}

interface RequestOptions extends RequestInit {
    skipAuth?: boolean
}

async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
    const token = localStorage.getItem('access_token')

    const headers = new Headers(options.headers)
    headers.set('Content-Type', 'application/json')
    if (token && !options.skipAuth) {
        headers.set('Authorization', `Bearer ${token}`)
    }

    const response = await fetch(`${BASE_URL}${path}`, { ...options, headers })

    if (response.status === 401 && !options.skipAuth && refreshHandler) {
        const refreshed = await refreshHandler()
        if (refreshed) {
            headers.set('Authorization', `Bearer ${localStorage.getItem('access_token')}`)
            return request<T>(path, { ...options, headers })
        }
    }

    if (!response.ok) {
        const errorBody = await response.json().catch(() => null)
        throw new Error(errorBody?.detail ?? `Request failed: ${response.status}`)
    }

    if (response.status === 204) return null as T
    return response.json()
}

export const http = {
    get: <T>(path: string, options?: RequestOptions) => request<T>(path, options),
    post: <T>(path: string, body: unknown, options?: RequestOptions) =>
        request<T>(path, { ...options, method: 'POST', body: JSON.stringify(body) }),
    patch: <T>(path: string, body: unknown, options?: RequestOptions) =>
        request<T>(path, { ...options, method: 'PATCH', body: JSON.stringify(body) }),
    delete: <T>(path: string, options?: RequestOptions) =>
        request<T>(path, { ...options, method: 'DELETE' }),
}
