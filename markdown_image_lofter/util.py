def get_file_hash(filepath: str) -> str:
    """
    if file is too big, read the first 8192 bytes.
    https://blog.csdn.net/qq_26373925/article/details/115409308
    """
    import hashlib
    from os.path import getsize
    file = open(filepath, 'rb')
    md5 = hashlib.md5()
    if getsize(filepath) > 3 * 1024 * 1024:
        md5.update(file.read(8192))
    else:
        md5.update(file.read())
    file.close()
    return md5.hexdigest()
