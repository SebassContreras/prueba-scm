
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import (

    get_current_user,
)
from app.database import get_session
from app.filters import apply_filters
from app.models import Item

router = APIRouter(prefix="/items", tags=["items"])


class SearchRequest(BaseModel):
    # TODO (candidato): diseña aquí el contrato de filtros estructurados.
    filters: str | None = None


class ItemOut(BaseModel):
    id: int
    sku: str
    status: str
    warehouse_id: int

    model_config = {"from_attributes": True}


@router.post("/search")
async def search_items(
    payload: SearchRequest,
    session: Annotated[AsyncSession, Depends(get_session)],
    _user: Annotated[str, Depends(get_current_user)],
) -> list[ItemOut]:
    stmt = select(Item)
    stmt = apply_filters(stmt, payload.filters)
    result = await session.execute(stmt)
    return [ItemOut.model_validate(i) for i in result.scalars().all()]


@router.patch("/{item_id}/status/{new_status}")
async def set_item_status(
    item_id: int,
    new_status: str,
    session: Annotated[AsyncSession, Depends(get_session)],
    _user: Annotated[str, Depends(get_current_user)],
):
    item = await session.get(Item, item_id)
    if item is None:
        return JSONResponse(
            status_code=200,
            content={"success": False,
                     "error": f"No existe el item {item_id}"},
        )
    item.status = new_status
    await session.commit()
    await session.refresh(item)
    return ItemOut.model_validate(item)
