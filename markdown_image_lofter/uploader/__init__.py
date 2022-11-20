from .aliyun_oss import AliyunOssUploader
from .qiniu_uploader import QiniuUploader
from .sm_ms import SmMsUploader


def get_uploader(
        name: str, kwargs: dict, **extra
) -> AliyunOssUploader | QiniuUploader | SmMsUploader:
    """
    args:
        name: literal['aliyun', 'sm.ms']
    """
    print(':v2', name)
    return {
        'aliyun': AliyunOssUploader,
        'qiniu' : QiniuUploader,
        'sm.ms' : SmMsUploader,
    }[name](**kwargs, **extra)
