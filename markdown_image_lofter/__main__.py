"""
python -m markdown_image_exchange --help
"""
import os.path

import lk_logger
from argsense import cli
from lk_utils.filesniff import normpath
from lk_utils.filesniff import relpath

lk_logger.setup(show_varnames=True)


@cli.cmd()
def main(filepath: str, dir_o: str = None, config: str = None):
    """
    args:
        filepath:
            the markdown file path (ends with [cyan]".md"[/]).
            [dim]╰[/dim] either relative or absolute path is ok.
    
    kwargs:
        dir_o (-d):
            output directory.
            [dim]╰[/dim] if not given, will use the same directory as the -
            input file. the filename will be "~.export.md".
        config (-c):
            the config file path (ends with [cyan]".yaml"[/]).
            [dim]╰[/dim] if not given, the built-in config -
            ([magenta]"./config.yaml"[/]) will be used.
    """
    file_i = normpath(filepath, force_abspath=True)
    if config:
        config = normpath(config, force_abspath=True)
    else:
        config = relpath('../config.yaml')
    if dir_o:
        dir_o = normpath(dir_o, force_abspath=True)
    else:
        dir_o = os.path.dirname(file_i)
    file_o = f'{dir_o}/{os.path.basename(file_i)[:-3]}.export.md'
    
    print(file_i, file_o, config, ':l')
    
    from .main import main
    main(file_i, file_o, config_path=config)


cli.run(main)
