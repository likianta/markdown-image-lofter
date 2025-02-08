"""
upload image to [sm.ms <https://sm.ms/>].

ref:

= https://doc.sm.ms/
= https://blog.csdn.net/qq_42951560/article/details/108618981
"""
import requests

from ._interface import Uploader
from ..util import get_file_hash


class SmMsUploader(Uploader):
    
    def __init__(self, secret_key: str, full_upload=False):
        """
        args:
            token: the api token.
                1. login to sm.ms
                2. visit 'dashboar' - 'api token'
                3. click 'generate secret token'
        """
        super().__init__('sm_ms.db', full_upload)
        self._url = 'https://sm.ms/api/v2/upload'
        self._header = {'Authorization': secret_key}
    
    def upload(self, filepath: str) -> str:
        hash_ = get_file_hash(filepath)
        if x := self._db.get(hash_):
            return x['url']
        with open(filepath, 'rb') as f:
            r = requests.post(
                self._url,
                files={'smfile': f},
                headers=self._header
            )
            # print(r.status_code, r.json(), ':ipl')
            '''
            r.json() -> dict
                succeed response:
                    {
                        'success': True,
                        'code': 'success',
                        'message': 'Upload success',
                        'data': {
                            'file_id': int,
                            'width': int,
                            'height': int,
                            'filename': str,
                            'storename': str,
                            'size': int,
                            'path': str path,
                            #   the path consists of:
                            #       '<yyyy>/<mm>/<dd>/<storename>'
                            'hash': str,
                            'url': str url,
                            'delete': str url,
                            'page': str url,
                        },
                        'RequestId': str,
                    }
                failed response:
                    {
                        'success': False,
                        'code': 'unauthorized' | 'invalid_source' | ...,
                        'message': <str the detailed info about this error>,
                        'RequestId': '...'
                    }
            '''
        
        json_ = r.json()
        if json_['success']:
            self._db[hash_] = json_['data']
            return json_['data']['url']
        elif json_['code'] == 'image_repeated':
            print(':v6p', 'image repeated but upload succeed')
            self._db[hash_] = {'url': json_['images']}
            return json_['images']
        else:
            print(json_, ':v8lp')
            raise Exception(json_['message'])
