import click

from os             import getcwd
from os.path        import join, exists
from difflib        import get_close_matches
from requests       import get

from tmsutils.utils import merge_sqlite_db, file_split

@click.group()
def cli():
    pass

@cli.command(help="generate .gitignore file for given Operating systems, IDEs or Programming Languages")
@click.argument('types', nargs=-1, required=True)
@click.option('--path', '-p', default=getcwd(), help='path where you want to generate .gitignore file')
@click.option('--replace', '-r', help='pass this option to replace the existing .gitignore file', is_flag=True)
def gi(path, types, replace):
    '''
    gi - it is a command line utility that helps you to generate .gitignore file for given filetypes
    USE:
        $ tms gi python go // or
        $ tms gi python,go

        but, in case of any such file type which is not supported
        eg: $ tms gi python3,abcdx
        you'll get suggestion for each keyword
        "python3" is invalid, try from "python"
        "abcdx" is invalid
    '''
    _types        = ','.join(types).split(',')
    _base_url     = 'https://www.toptal.com/developers/gitignore/api'
    valid_types   = get(f'{_base_url}/list').text.split('\n')
    valid_types   = ','.join(valid_types).split(',')

    invalid_types = set(_types) - set(valid_types)
    if invalid_types:
        for _ in invalid_types:
            _close_value = get_close_matches(_, valid_types)
            if _close_value:
                click.echo('"{}" is invalid, try from "{}"'.format(_, ','.join(_close_value)))
            else:
                click.echo('"{}" is invalid.'.format(_))
    else:
        _types   = ','.join(_types)
        response = get(f'{_base_url}/{_types}')
        with open(join(path, '.gitignore'), 'w' if replace else 'a') as f:
            f.write(response.text)

@cli.command(help='split text file (eg: txt, csv, etc) line-wise into multiple chunks')
@click.option('--chunk', '-c', default=10, help='Number of chunks you want to divide files into')
@click.argument('filepath', nargs=1, required=True)
def sf(filepath, chunk):
    if not exists(filepath):
        click.echo("file doesn't exist")
    else:
        file_split(filepath, parts=chunk)

@cli.command(help='merge .sqlite files in given directory of same schema')
@click.option('--path', '-p', default=getcwd(), help='path of the directory containing .sqlite file')
@click.option('--extension', '-e', default='sqlite3', help='database file extension (default=.sqlite3)')
def mdb(path, extension):
    result = merge_sqlite_db(path, extension=extension)
    click.echo(result) if result else click.echo('No sqlite3/db files found!')
