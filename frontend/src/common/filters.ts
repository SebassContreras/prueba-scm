export type FilterOperator = 'eq' | 'ne' | 'gt' | 'gte' | 'lt' | 'lte' | 'in'

export interface Filter {
    field: string
    operator: FilterOperator
    value: unknown
}

export interface SearchRequest {
    filters: Filter[]
}
