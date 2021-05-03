"""
HShake (https://github.com/gabliw)
Dataset Support
1. COCO Dataset
2. PASCAL VOC 2012
3. Cityscapes test
"""


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
    from pycocotools.coco import COCO

    NotImplemented


def pascal_loader():
    NotImplemented
