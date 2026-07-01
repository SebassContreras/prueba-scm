from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, select


from app.database import Base, SessionLocal, engine
from app.models import Item

from app.views import items_router, auth_router


SEED_ITEMS = [
    Item(sku="A1", status="pending", warehouse_id=1,
         created_at=datetime(2025, 1, 1)),
    Item(sku="A2", status="done", warehouse_id=1,
         created_at=datetime(2025, 1, 2)),
    Item(sku="B1", status="pending", warehouse_id=2,
         created_at=datetime(2025, 1, 3)),
    Item(sku="B2", status="cancelled", warehouse_id=2,
         created_at=datetime(2025, 1, 4)),
    Item(sku="C1", status="pending", warehouse_id=3,
         created_at=datetime(2025, 1, 5)),
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with SessionLocal() as session:
        existing = await session.scalar(select(func.count()).select_from(Item))
        if not existing:
            session.add_all(
                Item(
                    sku=i.sku,
                    status=i.status,
                    warehouse_id=i.warehouse_id,
                    created_at=i.created_at,
                )
                for i in SEED_ITEMS
            )
            await session.commit()
    yield


app = FastAPI(lifespan=lifespan)

# CORS abierto para que el frontend del candidato pueda conectarse sin fricción
# en local. En producción se restringiría a orígenes conocidos.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(items_router)
app.include_router(auth_router)
