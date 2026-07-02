export interface LoginRequest {
    username: string
    password: string
}

export interface TokenPair {
    access_token: string
    refresh_token: string
    token_type: string
}

export interface RefreshRequest {
    refresh_token: string
}
