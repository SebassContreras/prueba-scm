import { reactive, readonly } from 'vue'
import { login as loginService, logout as logoutService } from './service'
import type { LoginRequest } from './types'

const state = reactive({
    isAuthenticated: !!localStorage.getItem('access_token'),
})

async function login(payload: LoginRequest): Promise<void> {
    await loginService(payload)
    state.isAuthenticated = true
}

function logout(): void {
    logoutService()
    state.isAuthenticated = false
}

export const authStore = {
    state: readonly(state),
    login,
    logout,
}
