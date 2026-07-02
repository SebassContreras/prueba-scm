from pydantic import BaseModel
from typing import List, Any
from datetime import datetime


class Filter(BaseModel):
    field: str
    operator: str
    value: Any | None = None
    values: List[Any] | None = None


class SearchRequest(BaseModel):
    filters: List[Filter] | None = None


class ItemOut(BaseModel):
    id: int
    sku: str
    status: str
    warehouse_id: int
    created_at: datetime
    model_config = {"from_attributes": True}
