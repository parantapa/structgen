"""Generate memory layout C header."""

from importlib.resources import read_text

from jinja2 import Environment, StrictUndefined

from .sglang import ArrayType, ScalarType, Spec

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


def c_type(type_: ScalarType | ArrayType) -> str:
    return TYPE_CTYPE[type_.name]


def is_scalar(type_: ScalarType | ArrayType) -> bool:
    return isinstance(type_, ScalarType)


def make_env() -> Environment:
    """Make the jinja environment."""
    env = Environment(trim_blocks=True, lstrip_blocks=True, undefined=StrictUndefined)
    env.filters["c_type"] = c_type
    env.tests["scalar"] = lambda x: isinstance(x, ScalarType)
    return env


def make_c_header(spec: Spec, env: Environment) -> str:
    """Make the c header."""
    hdr_template = read_text("structgen", "c_hdr_template.jinja2")
    return env.from_string(hdr_template).render(spec=spec)

def make_c_body(spec: Spec, env: Environment) -> str:
    """Make the c code body."""
    hdr_template = read_text("structgen", "c_code_template.jinja2")
    return env.from_string(hdr_template).render(spec=spec)
