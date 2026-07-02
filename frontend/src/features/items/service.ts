import { http } from '../../api/http'
import type { Item, StatusUpdateResult } from './types'
import type { SearchRequest } from '../../common/filters'

const ENDPOINTS = {
    itemsSearch: '/items/search',
    itemStatus: (itemId: number, newStatus: string) => `/items/${itemId}/status/${newStatus}`,
} as const

export function searchItems(filters: SearchRequest['filters'] = []): Promise<Item[]> {
    return http.post<Item[]>(ENDPOINTS.itemsSearch, { filters })
}


export function setItemStatus(itemId: number, newStatus: string): Promise<StatusUpdateResult> {
    return http.patch<StatusUpdateResult>(ENDPOINTS.itemStatus(itemId, newStatus), {})
}
