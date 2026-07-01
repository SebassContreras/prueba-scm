
import pytest
from sqlalchemy import select

from app.models import Item
from app.schemas import Filter
from app.services.filters import apply_filters


def base_stmt():
    return select(Item)


def test_filtros_none_no_modifica_stmt():
    stmt = base_stmt()
    result = apply_filters(stmt, None)
    assert result is stmt


def test_filtros_vacios_no_modifica_stmt():
    stmt = base_stmt()
    result = apply_filters(stmt, [])
    assert result is stmt


def test_campo_invalido_lanza_error():
    f = Filter(field="precio", operator="=", value=100)
    with pytest.raises(ValueError, match="Campo no valido"):
        apply_filters(base_stmt(), [f])


def test_operador_invalido_lanza_error():
    f = Filter(field="sku", operator=">=", value="A")
    with pytest.raises(ValueError, match="Operador no valido"):
        apply_filters(base_stmt(), [f])


def test_exceso_de_filtros_lanza_error():
    max_fields = len(Item.__filterable_fields__)
    filters = [Filter(field="sku", operator="=", value="x")] * (max_fields + 1)
    with pytest.raises(
            ValueError,
            match="Se excede el número máximo de filtros permitidos"):
        apply_filters(base_stmt(), filters)
