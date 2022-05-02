"""Command line interface."""

from pathlib import Path
from pprint import pprint

import click

from .sglang import get_parser, SpecTransformer
from .code_gen import make_env, make_c_header, make_c_code, make_cffi_decl


@click.group()
def cli():
    """StructGen."""


@cli.command()
@click.argument("input")
def print_parsetree(input):
    """Print the parse tree for input."""
    text = Path(input).read_text()

    parser = get_parser()
    tree = parser.parse(text)
    print(tree.pretty())


@cli.command()
@click.argument("input")
def print_spec(input):
    """Print the specfication structure for input."""
    text = Path(input).read_text()

    parser = get_parser()
    tree = parser.parse(text)
    transformer = SpecTransformer()
    spec = transformer.transform(tree)
    pprint(spec)


@cli.command()
@click.argument("input")
def gen_code(input):
    """Print the c header structure for input."""
    input_file = Path(input)
    text = input_file.read_text()

    parser = get_parser()
    tree = parser.parse(text)
    transformer = SpecTransformer()
    spec = transformer.transform(tree)

    env = make_env()

    c_header = make_c_header(spec, env)
    c_header_file = input_file.parent / f"{spec.module}.h"
    c_header_file.write_text(c_header)

    c_code = make_c_code(spec, env)
    c_code_file = input_file.parent / f"{spec.module}.c"
    c_code_file.write_text(c_code)

    cffi_decl = make_cffi_decl(spec, env)
    cffi_decl_file = input_file.parent / f"{spec.module}_cffi_decl.py"
    cffi_decl_file.write_text(cffi_decl)
