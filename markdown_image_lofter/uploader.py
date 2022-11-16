"""
upload image to [sm.ms <https://sm.ms/>].

ref:

= https://doc.sm.ms/
= https://blog.csdn.net/qq_42951560/article/details/108618981
"""
import requests


class Uploader:
    
    def __init__(self, token: str):
        """
        args:
            token: the api token.
                1. login to sm.ms
                2. visit 'dashboar' - 'api token'
                3. click 'generate secret token'
            
        
        """
        self.url = 'https://sm.ms/api/v2/upload'
        self._header = {'Authorization': token}
    
    def upload(self, filepath: str) -> dict:
        with open(filepath, 'rb') as f:
            r = requests.post(self.url,
                              files={'smfile': f},
                              headers=self._header)
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
            return json_['data']
        elif json_['code'] == 'image_repeated':
            print(':v3p', 'image repeated but upload succeed')
            # print(':v', json_['images'])
            return {'url': json_['images']}
        else:
            print(json_, ':v4lp')
            raise Exception(json_['message'])
