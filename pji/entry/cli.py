import click
from click.core import Context, Option

from ..config.meta import __TITLE__, __VERSION__, __AUTHOR__, __AUTHOR_EMAIL__


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


# noinspection PyUnusedLocal
def validate_concurrency(ctx: Context, param: Option, value: int):
    if value > 0:
        return value
    else:
        raise ValueError("Concurrency should be no less than 1.")


CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help']
)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-v', '--version', is_flag=True,
              callback=print_version, expose_value=False, is_eager=True,
              help="Show package's version information.")
def cli():
    pass
