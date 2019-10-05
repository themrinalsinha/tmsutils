import click

from os       import getcwd
from os.path  import join
from difflib  import get_close_matches
from requests import get

@click.group()
def cli():
    pass

@cli.command(help="generate .gitignore file for given Operating systems, IDEs or Programming Languages")
@click.argument('types', nargs=-1, required=True)
@click.option('--path', default=getcwd(), help='path where you want to generate .gitignore file')
def gi(path, types):
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
    valid_types   = get('https://gitignore.io/api/list').text.split('\n')
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
        response = get('http://gitignore.io/api/{}'.format(_types))
        with open(join(path, '.gitignore'), 'w') as f:
            f.write(response.text)
