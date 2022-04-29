"""Structgen Language Parser."""

from dataclasses import dataclass
from importlib.resources import read_text

from lark import Lark, Transformer  # type: ignore


@dataclass
class ScalarType:
    name: str


@dataclass
class ArrayType:
    name: str
    length_constant: str


@dataclass
class Column:
    name: str
    type_: ScalarType | ArrayType


@dataclass
class Table:
    name: str
    columns: list[Column]


@dataclass
class Constant:
    name: str
    value: int


@dataclass
class Spec:
    module: str
    constants: list[Constant]
    tables: list[Table]


class SpecTransformer(Transformer):  # type: ignore
    def typename(self, children):
        return children[0].value

    def scalartype(self, children):
        return ScalarType(children[0])

    def arraytype(self, children):
        return ArrayType(children[0], children[1].value)

    def column(self, children):
        return Column(children[0].value, children[1])

    def columns(self, children):
        return list(children)

    def table(self, children):
        return Table(children[0].value, children[1])

    def constant(self, children):
        return Constant(children[0].value, int(children[1].value))

    def tables(self, children):
        return {t.name: t for t in children}

    def constants(self, children):
        return {c.name: c for c in children}

    def spec(self, children):
        return Spec(children[0].value, children[1], children[2])


def get_parser() -> Lark:
    """Return the parser."""
    grammar = read_text("structgen", "sglang_grammar.lark")
    parser = Lark(grammar, start="spec", parser="lalr")
    return parser


