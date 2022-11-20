import typing as t
from os.path import basename

import qiniu

from ._interface import Uploader
from ..util import get_file_hash


class T:
    Model = t.TypedDict('Model', {
        'id'  : str,
        'name': str,
        'url' : str,
    })


class QiniuUploader(Uploader):
    
    def __init__(
            self,
            access_key: str,
            secret_key: str,
            bucket_name: str,
            domain_name: str,
            full_upload=False,
    ):
        """
        warning: the test domain will be expired after 30 days. please check it
        manually if you find the link not works.
        """
        super().__init__('qiniu_oss.db', full_upload)
        self._auth = qiniu.Auth(access_key, secret_key)
        self._bucket_name = bucket_name
        self._domain_name = domain_name
    
    def upload(self, filepath: str) -> str:
        name = basename(filepath)
        hash_ = get_file_hash(filepath)
        
        model: T.Model
        if not self._is_full_upload and (model := self._db.get(hash_)):
            print('use cached temp url', name)
            return model['url']
        
        src, dst = filepath, name
        token = self._auth.upload_token(self._bucket_name, dst)
        qiniu.put_file(token, dst, src)
        
        self._db[hash_] = {
            'id'  : hash_,
            'name': name,
            'url' : (out := f'http://{self._domain_name}/{name}'),
        }
        self._db.sync()
        return out
