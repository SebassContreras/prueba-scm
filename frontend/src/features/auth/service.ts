import { http, setRefreshHandler } from '../../api/http'
import type { LoginRequest, TokenPair } from './types'


const ENDPOINTS = {
    login: '/auth/login/',
    refresh: '/auth/refresh/',
} as const


export async function login(payload: LoginRequest): Promise<void> {
    const tokens = await http.post<TokenPair>(ENDPOINTS.login, payload, { skipAuth: true })
    localStorage.setItem('access_token', tokens.access_token)
    localStorage.setItem('refresh_token', tokens.refresh_token)
}

export function logout(): void {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
}

export async function refreshAccessToken(): Promise<boolean> {
    const refresh = localStorage.getItem('refresh_token')
    if (!refresh) return false

    try {
        const { access } = await http.post<{ access: string }>(
            ENDPOINTS.refresh,
            { refresh },
            { skipAuth: true }
        )
        localStorage.setItem('access_token', access)
        return true
    } catch {
        logout()
        return false
    }
}

setRefreshHandler(refreshAccessToken)
