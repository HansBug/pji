from typing import List

import click
from click.core import Context, Option

from .environ import _load_environ
from .event import _DEFAULT_FILENAME, _load_dispatch_getter
from .exception import _raise_exception_with_exit_code
from ...config.meta import __TITLE__, __VERSION__, __AUTHOR__, __AUTHOR_EMAIL__


def print_version(ctx: Context, param: Option, value: bool) -> None:
    """
    Print version information of cli
    :param ctx: click context
    :param param: current parameter's metadata
    :param value: value of current parameter
    """
    if not value or ctx.resilient_parsing:
        return
    click.echo('{title}, version {version}.'.format(title=__TITLE__.capitalize(), version=__VERSION__))
    click.echo('Developed by {author}, {email}.'.format(author=__AUTHOR__, email=__AUTHOR_EMAIL__))
    ctx.exit()


CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help']
)

_DEFAULT_TASK = 'main'


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-v', '--version', is_flag=True,
              callback=print_version, expose_value=False, is_eager=True,
              help="Show package's version information.")
@click.option('-s', '--script', type=click.Path(exists=True, readable=True),
              help='Path of pji script.', default=_DEFAULT_FILENAME, show_default=True)
@click.option('-t', '--task', type=str, help='Task going to be executed.',
              default=_DEFAULT_TASK, show_default=True)
@click.option('-e', '--environ', type=str, multiple=True,
              help='Environment variables (loaded before global config).')
@click.option('-E', '--environ_after', type=str, multiple=True,
              help='Environment variables (loaded after global config).')
def cli(script: str, task: str, environ: List[str], environ_after: List[str]):
    _dispatch_getter = _load_dispatch_getter(script)
    _dispatch = _dispatch_getter(
        environ=_load_environ(environ),
        environ_after=_load_environ(environ_after),
    )
    _success, _result = _dispatch(task)

    if _success:
        click.echo(click.style('Task success.', fg='green'))
    else:
        click.echo(click.style('Task failed.', fg='red'))
        raise _raise_exception_with_exit_code(1, 'task failed.')
