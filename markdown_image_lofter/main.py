import os.path
from collections import defaultdict

from lk_utils import fs

from .extractor2 import extract_image_urls
from .uploader import get_uploader


def main(
    file_i: str,
    file_o: str = None,
    overwrite_exists: bool = True,
    config_path: str = None,
    full_upload: bool = False,
    html_tag_format: bool = False,
):
    """
    extract images from `file_i`, upload them, then replace them with urls,
    finally write the result to `file_o`.

    args:
        html_tag_format: use `<img src="...">` instead of `![...](...)`.
    """
    if not file_o:
        file_o = file_i.rsplit(".", 1)[0] + ".export.md"
    if not overwrite_exists and os.path.exists(file_o):
        raise FileExistsError(f"{file_o} already exists!")
    if not config_path:
        config_path = fs.xpath("../config.yaml")

    dir_i = os.path.dirname(file_i)
    doc_i = fs.load(file_i)

    config = fs.load(config_path)
    uploader = get_uploader(
        config["image_hosting"]["name"],
        config["image_hosting"]["kwargs"],
        full_upload=full_upload,
    )

    token_locations = defaultdict(list)
    #   {int row: [(int col_start, int col_end), ...]}
    image_urls = {}
    #   {tuple[row, col]: str web_url, ...}
    #       image_hash: calculated from local image file.
    #       web_url: after we upload the image to the remote server, we get the
    #           web url.

    for (row_start, row_end), (col_start, col_end), (
        src,
        alt,
        title,
    ) in extract_image_urls(doc_i):
        print("(row, col) = {}".format((row_start, col_start)), src, ":v")

        # check if local image
        if src.startswith("http"):  # PERF: this is not reliable enough.
            print("skip web image", src)
            continue

        token_locations[row_start].append((col_start, col_end))
        if os.path.isabs(src):
            filepath = fs.normpath(src)
        else:
            filepath = fs.normpath(f"{dir_i}/{src}", force_abspath=True)
        link = uploader.upload(filepath)
        image_urls[(row_start, col_start)] = link
        print(f"{src} -> {link}", ":v2")

    # -------------------------------------------------------------------------

    def replace_image_holders() -> str:
        # tip: replace from last to first (in reversed order)
        doc_m = doc_i.splitlines()  # '_m' means 'mediate state'
        for row_start in sorted(token_locations.keys(), reverse=True):
            for col_start, col_end in sorted(
                token_locations[row_start], key=lambda x: x[0], reverse=True
            ):
                print(row_start, col_start, col_end, ":v")
                head, tail = (
                    doc_m[row_start][:col_start],
                    doc_m[row_start][col_end + 1 :],
                )
                url = image_urls[(row_start, col_start)]
                if html_tag_format:
                    body = f'<img src="{url}">'
                else:
                    body = f"![]({url})"
                doc_m[row_start] = head + body + tail
        return "\n".join(doc_m)

    doc_o = replace_image_holders()
    fs.dump(doc_o, file_o)
    print("see output at [green]{}[/]".format(file_o), ":rv2t")
