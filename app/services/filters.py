from typing import List
from app.models import Item
from app.schemas import Filter

MAX_ROWS = 500

OPERATORS = {
    "=": lambda col, val: col == val,
    "!=": lambda col, val: col != val,
    ">": lambda col, val: col > val,
    "<": lambda col, val: col < val,
    "like": lambda col, val: col.like(val),
    "in": lambda col, val: col.in_(val),
    "is null": lambda col, val: col.is_(None),
}

NEEDS_VALUE = {"=", "!=", ">", "<", "like"}
NEEDS_VALUES_LIST = {"in"}
NEEDS_NOTHING = {"is null"}


def _validate_field(field: str, allowed_fields: set):
    if field not in allowed_fields:
        raise ValueError(f"Campo no válido: {field}")


def _validate_operator(operator: str):
    if operator not in OPERATORS:
        raise ValueError(f"Operador no válido: {operator}")


def _validate_value(f: Filter):
    if f.operator in NEEDS_VALUE and f.value is None:
        raise ValueError(f"Operador '{f.operator}' requiere 'value'")
    if f.operator in NEEDS_VALUES_LIST and not f.values:
        raise ValueError(f"Operador '{f.operator}' requiere 'values'")
    if f.operator in NEEDS_NOTHING and (f.value is not None or f.values is not None):
        raise ValueError(
            f"Operador '{f.operator}' no requiere 'value' ni 'values'")


def _validate_duplicate(f: Filter, seen: set):
    key = (f.field, f.operator)
    if key in seen:
        raise ValueError(f"Filtro duplicado: '{f.field}' con '{f.operator}'")
    seen.add(key)


def apply_filters(stmt, filters: List[Filter] | None):
    if not filters:
        return stmt

    allowed_fields = Item.__filterable_fields__

    if len(filters) > len(allowed_fields):
        raise ValueError("Se excede el número máximo de filtros permitidos.")

    seen = set()
    for f in filters:
        _validate_field(f.field, allowed_fields)
        _validate_operator(f.operator)
        _validate_duplicate(f, seen)
        _validate_value(f)

        column = getattr(Item, f.field)
        value = f.values if f.operator == "in" else f.value
        stmt = stmt.where(OPERATORS[f.operator](column, value))

    return stmt.limit(MAX_ROWS)
