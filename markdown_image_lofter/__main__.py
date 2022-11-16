import os.path

import lk_logger
from argsense import cli
from lk_utils.filesniff import normpath
from lk_utils.filesniff import xpath

lk_logger.setup(quiet=True, show_varnames=True)


@cli.cmd()
def main(filepath: str, dir_o: str = None, config: str = None,
         full_upload=False):
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
        full_upload (-f):
    """
    file_i = normpath(filepath, force_abspath=True)
    if config:
        config = normpath(config, force_abspath=True)
    else:
        config = xpath('../config.yaml')
    if dir_o:
        dir_o = normpath(dir_o, force_abspath=True)
    else:
        dir_o = os.path.dirname(file_i)
    file_o = f'{dir_o}/{os.path.basename(file_i)[:-3]}.export.md'
    
    print(file_i, file_o, config, ':l')
    
    from .main import main
    main(file_i, file_o, config_path=config, full_upload=full_upload)


cli.run(main)
