from typing import List
from app.models import Item
from app.schemas import Filter

MAX_ROWS = 500


def apply_filters(stmt, filters: List[Filter] | None):
    if not filters:
        return stmt

    allowed_fields = Item.__filterable_fields__

    max_filters = len(allowed_fields)
    if len(filters) > max_filters:
        raise ValueError(
            "Se excede el número máximo de filtros permitidos.")

    operators = {
        "=": lambda col, val: col == val,
        "!=": lambda col, val: col != val,
        ">": lambda col, val: col > val,
        "<": lambda col, val: col < val,
        "like": lambda col, val: col.like(val),
        "in": lambda col, val: col.in_(val),
        "is null": lambda col, val: col.is_(None),
    }

    for f in filters:
        if f.field not in allowed_fields:
            raise ValueError(f"Campo no valido: {f.field}")

        if f.operator not in operators:
            raise ValueError(f"Operador no valido: {f.operator}")

        column = getattr(Item, f.field)
        value = f.values if f.operator == "in" else f.value

        stmt = stmt.where(operators[f.operator](column, value))

    return stmt.limit(MAX_ROWS)
