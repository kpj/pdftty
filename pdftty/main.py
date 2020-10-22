import click

from .controller import Controller


@click.command(help='View PDFs in the terminal.')
@click.option('--page', default=1, help='Page of PDF to open.')
@click.argument('fname', type=click.Path(exists=True, dir_okay=False))
def main(page: int, fname: str) -> None:
    Controller(fname).main(page)


if __name__ == '__main__':
    main()
