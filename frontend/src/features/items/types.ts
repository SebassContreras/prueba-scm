import type { StatusUpdateError } from "../../common/response"

export interface Item {
    id: number
    sku: string
    status: string
    warehouse_id: number
    created_at: string
}

export type StatusUpdateResult = Item | StatusUpdateError
