# -*- coding: utf-8 -*-

from functools import singledispatch

from . import parse_date


map_redshift = {
    "bigint": "BIGINT",
    "boolean": "BOOL",
    "character": "VARCHAR",
    "character varying": "VARCHAR",
    "date": "DATE",
    "double precision": "FLOAT8",
    "integer": "INT",
    "numeric": "FLOAT8",
    "smallint": "SMALLINT",
    "timestamp without time zone": "TIMESTAMP",
}


def type_set(t: list):
    return set(map(type, t))


def int_in_bounds(num_bits, val):
    n_max = (2 ** num_bits) // 2
    if val > 0:
        n_max -= 1
    return abs(val) <= n_max


@singledispatch
def set_dtype(val, **kwargs):
    return f"UNKNOWN_{type(val).__name__}"


@set_dtype.register
def __str_dtype(val: str, infer_date: bool = False):

    if any(c.isdigit() for c in val):
        dtype = parse_date.guess_type(val)
        if dtype:
            return dtype
    return "VARCHAR"


@set_dtype.register
def __float_dtype(val: float, **kwargs):

    num_bits = (64 - 15, 32 - 6)
    dtypes = ("FLOAT8", "FLOAT4")

    dtype = None
    for n, dtype in zip(num_bits, dtypes):
        if abs(val) >= 2 ** n // 2:
            break
    return dtype


@set_dtype.register
def __int_dtype(val: int, **kwargs):

    if int_in_bounds(16, val):
        dtype = "SMALLINT"
    elif int_in_bounds(32, val):
        dtype = "INT"
    elif int_in_bounds(64, val):
        dtype = "BIGINT"
    else:
        raise ValueError(f"Input exceeds integer max number of bits: {val}")
    return dtype


@set_dtype.register
def __bool_dtype(val: bool, **kwargs):
    return "BOOL"
