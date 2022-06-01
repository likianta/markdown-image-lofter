from hot_shelve import FlatShelve
from lk_utils import relpath

data_dir = relpath('../../data')

image_db = FlatShelve(f'{data_dir}/uploaded_images.db')

print(image_db.to_dict(), ':l')
