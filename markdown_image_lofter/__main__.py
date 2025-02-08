import lk_logger
from argsense import cli
from lk_utils import fs

lk_logger.setup(quiet=True, show_varnames=True)


@cli.cmd()
def main(
    filepath: str,
    dir_o: str = None,
    config: str = None,
    full_upload: bool = False,
    html_tag_format: bool = False,
):
    """
    params:
        filepath:
            the markdown file path (ends with [cyan]".md"[/]).
            [dim]╰[/dim] either relative or absolute path is ok.
        dir_o (-d):
            output directory.
            [dim]╰[/dim] if not given, will use the same directory as the -
            input file. the filename will be "~.export.md".
        config (-c):
            the config file path (ends with [cyan]".yaml"[/]).
            [dim]╰[/dim] if not given, the built-in config -
            ([magenta]"./config.yaml"[/]) will be used.
        full_upload (-f):
        html_tag_format (-t):
            if configured aliyun oss as image hosting, csdn cannot trans-save -
            the images. (see -
            https://blog.csdn.net/m0_51562352/article/details/127918355)
            enable this option to use html tag format, which can be loaded in -
            csdn.
            be aware that enabling this will disable csdn trans-saving -
            function. we are finding a way to solve it.
    """
    file_i = fs.abspath(filepath)
    if config:
        config = fs.abspath(config)
    else:
        config = fs.xpath("../config.yaml")
    if dir_o:
        dir_o = fs.abspath(dir_o)
    else:
        dir_o = fs.parent(file_i)
    if full_upload:
        print(":v3", "you are using full upload mode!")
    file_o = '{}/{}.export.md'.format(dir_o, fs.barename(file_i))
    
    print(file_i, file_o, config, ":v2")
    
    from .main import main
    main(
        file_i,
        file_o,
        config_path=config,
        full_upload=full_upload,
        html_tag_format=html_tag_format,
    )


if __name__ == "__main__":
    # pox -m markdown_image_lofter -h
    cli.run(main)
