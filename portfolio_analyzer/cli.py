from decimal import Decimal

import click
from tabulate import tabulate

from .analyzer import get_summary


@click.group()
def cli():
    pass


@cli.command()
@click.option("--path", "-p", help="path to the CSV file with data", required=True)
@click.option("--value", "-v", help="current portfolio value", required=True, type=Decimal)
def summary(path, value):
    summary = get_summary(path, value)
    click.echo(tabulate(summary, tablefmt="fancy_grid"))


@cli.command()
@click.option("--path", "-p", help="path to the CSV file with data")
@click.option("--tickers", "-t", default="", help="filter to only these tickers, leave empty for all")
def details(path, tickers):
    click.echo(path)
    click.echo(tickers)


def main():
    cli()