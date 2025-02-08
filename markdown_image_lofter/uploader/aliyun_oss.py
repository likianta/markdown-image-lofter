import typing as t
from os.path import basename
from time import time

from lk_utils import timestamp
from oss2 import Auth
from oss2 import Bucket

from ._interface import Uploader
from ..util import get_file_hash


class T:
    Model = t.TypedDict('Model', {
        'id'              : str,
        'name'            : str,
        'url'             : str,
        'temp_url'        : str,
        'temp_url_expires': int,
    })


class AliyunOssUploader(Uploader):
    expires = 3600 * 24
    
    def __init__(
            self,
            access_key: str,
            secret_key: str,
            bucket_name: str,
            endpoint: str,
            full_upload=False,
    ):
        super().__init__('aliyun_oss.db', full_upload)
        self._auth = Auth(access_key, secret_key)
        self._bucket = Bucket(self._auth, endpoint, bucket_name)
    
    def make_link(self, key: str, expires=3600 * 24) -> str:
        """ make link for sharing. """
        return self._bucket.sign_url('GET', key, expires, slash_safe=True)
    
    def upload(self, filepath: str) -> str:
        name = basename(filepath)
        hash = get_file_hash(filepath)
        link = '{}/{}'.format(timestamp('y-m'), name)
        
        if not self._is_full_upload:
            model: T.Model
            if model := self._db.get(hash):
                now = int(time())
                if model['temp_url_expires'] < now:
                    print('refresh temp url')
                    model['temp_url'] = self.make_link(
                        model['url'], self.expires
                    )
                    model['temp_url_expires'] = now + self.expires
                    self._db.sync()
                else:
                    print('use cached temp url')
                return model['temp_url']
        
        self._bucket.put_object_from_file(link, filepath)
        print('upload done', link)
        
        self._db[hash] = {
            'id'              : hash,
            'name'            : name,
            'url'             : link,
            'temp_url'        : (out := self.make_link(link, self.expires)),
            'temp_url_expires': int(time()) + self.expires,
        }
        self._db.sync()
        return out
