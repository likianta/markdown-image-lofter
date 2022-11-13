import hashlib
import os.path
from collections import defaultdict

from hot_shelve import FlatShelve
from lk_utils import dumps
from lk_utils import loads
from lk_utils import relpath
from lk_utils.filesniff import normpath

# from .extractor import extract_image_urls
from .extractor2 import extract_image_urls
from .uploader import Uploader


def main(file_i: str, file_o: str = None, overwrite_exists=True,
         config_path=None):
    """
    extract images from `file_i`, upload them, then replace them with urls,
    finally write the result to `file_o`.
    """
    if not file_o:
        file_o = file_i.rsplit('.', 1)[0] + '.export.md'
    if not overwrite_exists and os.path.exists(file_o):
        raise FileExistsError(f'{file_o} already exists!')
    if not config_path:
        config_path = relpath('../config.yaml')
    
    dir_i = os.path.dirname(file_i)
    doc_i = loads(file_i)
    
    database = FlatShelve(relpath('../data/uploaded_images.db'))
    config = loads(config_path)
    # noinspection PyTypeChecker
    uploader = Uploader(token=config['image_hosting']['sm.ms']['secret_token'])
    
    token_locations = defaultdict(list)
    #   {int row: [(int col_start, int col_end), ...]}
    image_urls = {}
    #   {tuple[row, col]: str web_url, ...}
    #       image_hash: calculated from local image file.
    #       web_url: after we upload the image to the remote server, we get the
    #           web url.
    
    for (
            (row_start, row_end),
            (col_start, col_end),
            (src, alt, title)
    ) in extract_image_urls(doc_i):
        print('(row, col) = {}'.format((row_start, col_start)), src, ':v')
        
        # check if local image
        if src.startswith('http'):  # PERF: this is not reliable enough.
            print('skip web image', src)
            continue
        
        token_locations[row_start].append((col_start, col_end))
        if os.path.isabs(src):
            filepath = normpath(src)
        else:
            filepath = normpath(f'{dir_i}/{src}', force_abspath=True)
        hash_ = get_file_hash(filepath)
        if hash_ in database:
            print('reuse cache', src, ':v')
            url = image_urls[(row_start, col_start)] = database[hash_]['url']
        else:
            print('uploading', src)
            data = uploader.upload(filepath)
            database[hash_] = data
            url = image_urls[(row_start, col_start)] = data['url']
        print(src, hash_, url, ':v2')

    # replace image holders
    # tip: replace from last to first (in reversed order)
    doc_m = doc_i.splitlines()  # '_m' means 'mediate state'
    for row_start in sorted(token_locations.keys(), reverse=True):
        for (col_start, col_end) in sorted(
                token_locations[row_start], key=lambda x: x[0], reverse=True
        ):
            print(row_start, col_start, col_end, ':v')
            doc_m[row_start] = '{}{}{}'.format(
                doc_m[row_start][:col_start],
                '![]({})'.format(image_urls[(row_start, col_start)]),
                doc_m[row_start][col_end:]
            )
    doc_o = '\n'.join(doc_m)
    dumps(doc_o, file_o)
    print('see output at [green]{}[/]'.format(file_o), ':rv2t')
    
    database.close()


def get_file_hash(filepath: str):
    """
    https://blog.csdn.net/qq_26373925/article/details/115409308
    
    note: if file is too big, read the first 8192 bytes.
    """
    with open(filepath, 'rb') as file:
        md5 = hashlib.md5()
        if os.path.getsize(filepath) > 3 * 1024 * 1024:
            md5.update(filepath.encode('utf-8') + file.read(8192))
        else:
            md5.update(filepath.encode('utf-8') + file.read())
    return md5.hexdigest()
