"""
HShake (https://github.com/gabliw)
Dataset Support
1. COCO Dataset
2. PASCAL VOC 2012
3. Cityscapes test
"""

import os


def data_loader(**kwargs):
    path = kwargs['path']
    dn = kwargs['dataset']

    if dn == 'coco':
        coco_loader()
    elif dn == 'pascal voc':
        NotImplemented
    elif dn == 'custom':
        NotImplemented

    NotImplemented


def coco_loader():
    from torch.utils.data import Dataset, DataLoader
    from pycocotools.coco import COCO

    class COCO_Dataset(Dataset):
        def __init__(self, root_dir='D:\Data\coco', set_name='val2017', split='TRAIN'):
            super().__init__()
            self.root_dir = root_dir
            self.set_name = set_name
            self.coco = COCO(os.path.join(self.root_dir, 'annotations', 'instances_' + self.set_name + '.json'))
    NotImplemented


def pascal_loader():
    NotImplemented


def cityscapes_loader():
    NotImplemented