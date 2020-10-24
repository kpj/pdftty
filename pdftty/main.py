import click

from .controller import Controller


@click.command(help='View PDFs in the terminal.')
@click.option('--page', default=1, help='Page of PDF to open.')
@click.option(
    '--render-engine', default='ANSI',
    type=click.Choice(['ANSI', 'CACA'], case_sensitive=False),
    help='Which engine to use to render PDF page as text.')
@click.argument(
    'fname', type=click.Path(exists=True, dir_okay=False),
    metavar='<file>')
def main(page: int, fname: str, render_engine: str) -> None:
    Controller().main(fname, page, render_engine)


if __name__ == '__main__':
    main()
