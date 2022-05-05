"""
python -m markdown_image_exchange --help
"""
import os.path

import lk_logger
from lk_utils.filesniff import normpath
from lk_utils.filesniff import relpath
from rich_click import rich_click
from rich_click import typer

rich_click.USE_RICH_MARKUP = True
lk_logger.setup(show_varnames=True)


def cli(
        filepath: str = typer.Argument(
            ..., help='the markdown file path (ends with [cyan]".md"[/]).\n\n'
                      '[dim]╰[/dim] either relative or absolute path is ok.',
            exists=True, file_okay=True, dir_okay=False,
        ),
        dir_o: str = typer.Option(
            None, help='output directory.\n\n'
                       '[dim]╰[/dim] if not given, will use the same directory '
                       'as the input file. the filename will be "~.export.md".',
        ),
        config: str = typer.Option(
            None, help=f'the config file path (ends with [cyan]".yaml"[/]).\n\n'
                       f'[dim]╰[/dim] if not given, the built-in config '
                       f'([magenta]{relpath("../config.yaml")}[/]) will be used.'
        )
):
    file_i = normpath(filepath, force_abspath=True)
    if config:
        config = normpath(config, force_abspath=True)
    if dir_o:
        dir_o = normpath(dir_o, force_abspath=True)
    else:
        dir_o = os.path.dirname(file_i)
    file_o = f'{dir_o}/{os.path.basename(file_i)[:-3]}.export.md'
    
    print(file_i, file_o, config, ':l')
    
    from .main import main
    main(file_i, file_o, config_path=config)


typer.run(cli)
