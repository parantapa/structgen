"""Command line interface."""

from pathlib import Path
from pprint import pprint

import click

from .sglang import get_parser, SpecTransformer
from .c_gen import make_env, make_c_header, make_c_body


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
def print_c_header(input):
    """Parse the c header structure for input."""
    text = Path(input).read_text()

    parser = get_parser()
    tree = parser.parse(text)
    transformer = SpecTransformer()
    spec = transformer.transform(tree)

    env = make_env()
    c_header = make_c_header(spec, env)
    print(c_header)

@cli.command()
@click.argument("input")
def print_c_body(input):
    """Parse the c code body structure for input."""
    text = Path(input).read_text()

    parser = get_parser()
    tree = parser.parse(text)
    transformer = SpecTransformer()
    spec = transformer.transform(tree)

    env = make_env()
    c_body = make_c_body(spec, env)
    print(c_body)
