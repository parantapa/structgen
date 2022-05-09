"""Code generation module."""

from importlib.resources import read_text

from jinja2 import Environment, StrictUndefined

from .sglang import ArrayType, ScalarType, Spec, Table

TYPE_CTYPE = {
    "u8": "uint8_t",
    "u16": "uint16_t",
    "u32": "uint32_t",
    "u64": "uint64_t",
    "i8": "int8_t",
    "i16": "int16_t",
    "i32": "int32_t",
    "i64": "int64_t",
}

TYPE_PRINTF_FMT = {
    "u8": "PRIu8",
    "u16": "PRIu16",
    "u32": "PRIu32",
    "u64": "PRIu64",
    "i8": "PRIi8",
    "i16": "PRIi16",
    "i32": "PRIi32",
    "i64": "PRIi64",
}


def c_type(type_: ScalarType | ArrayType) -> str:
    return TYPE_CTYPE[type_.name]


def is_scalar(type_: ScalarType | ArrayType) -> bool:
    return isinstance(type_, ScalarType)


def printf_fmt(
    tabvar: str, idxvar: str, table: Table, spec: Spec
) -> tuple[str, str, str]:
    hdrs, fmts, cols = [], [], []
    for column in table.columns:
        if is_scalar(column.type_):
            hdr = column.name
            fmt = TYPE_PRINTF_FMT[column.type_.name]
            col = f"{tabvar}->{column.name}[{idxvar}]"

            hdrs.append(hdr)
            fmts.append(fmt)
            cols.append(col)
        else:
            length_constant = column.type_.length_constant  # type: ignore
            length = spec.constants[length_constant].value
            for i in range(length):
                hdr = f"{column.name}_{i}"
                fmt = TYPE_PRINTF_FMT[column.type_.name]
                col = f"{tabvar}->{column.name}[{i}][{idxvar}]"

                hdrs.append(hdr)
                fmts.append(fmt)
                cols.append(col)

    hdrs = ",".join(hdrs)
    fmts = '"%" ' + ' ",%" '.join(fmts)
    cols = ", ".join(cols)

    return hdrs, fmts, cols


def make_env() -> Environment:
    """Make the jinja environment."""
    env = Environment(trim_blocks=True, lstrip_blocks=True, undefined=StrictUndefined)
    env.filters["c_type"] = c_type
    env.tests["scalar"] = lambda x: isinstance(x, ScalarType)
    env.globals.update({"printf_fmt": printf_fmt})
    return env


def make_c_header(spec: Spec, env: Environment) -> str:
    """Make the c header."""
    hdr_template = read_text("structgen", "c_hdr_template.jinja2")
    return env.from_string(hdr_template).render(spec=spec)


def make_c_code(spec: Spec, env: Environment) -> str:
    """Make the c code."""
    hdr_template = read_text("structgen", "c_code_template.jinja2")
    return env.from_string(hdr_template).render(spec=spec)


def make_cffi_decl(spec: Spec, env: Environment) -> str:
    """Make the cffi declarations."""
    hdr_template = read_text("structgen", "cffi_decl_template.jinja2")
    return env.from_string(hdr_template).render(spec=spec)
