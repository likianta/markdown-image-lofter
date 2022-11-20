from hot_shelve import FlatShelve
from lk_utils import xpath


class Uploader:
    
    def __init__(self, db_name: str, full_upload=False):
        assert db_name.endswith('.db')
        self._db = FlatShelve(xpath('../../data/{}'.format(db_name)))
        self._is_full_upload = full_upload
    
    def upload(self, filepath: str) -> str:
        raise NotImplementedError
    
    @staticmethod
    def _update_progress(
            description: str,
            bytes_consumed: int, total_bytes: int
    ) -> None:
        print('{}: {:.2%}'.format(
            description,
            bytes_consumed / total_bytes
        ), end='\r')
