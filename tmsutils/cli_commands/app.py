import click

from os       import getcwd
from requests import get

@click.group()
def cli():
    pass

# Set nargs=-1 for unli

@cli.command(help="generate .gitignore file for given Operating systems, IDEs or Programming Languages")
@click.argument('types', nargs=-1, required=True)
@click.option('--path', default=getcwd(), help='path where you want to generate .gitignore file')
def gitignore(path, types):
    _types = ','.join(types)
    print(path, _types)
