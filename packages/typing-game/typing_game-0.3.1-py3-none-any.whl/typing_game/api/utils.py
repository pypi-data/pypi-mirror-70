__all__ = (
    'SafeMember', 'ABCSafeMember',
    'ShowTestDescription',
    'cached_property', 'after_end',
)

from unittest import TestCase
import abc
from contextlib import contextmanager
from typing import Callable
import sys


class MetaMemberControl(type):
    """
    - If you want to modify the variable of the member, you must add prefix with _ on it.
    - If you want to get the variable of the member, you can pass the name without the prefix that with underscore (_)
    """
    __slots__ = ()

    def __new__(mcs, f_cls_name, f_cls_parents, f_cls_attr,
                meta_args=None, meta_options=None):

        original_getattr = f_cls_attr.get('__getattribute__')
        original_setattr = f_cls_attr.get('__setattr__')

        def init_getattr(self, item):
            if not item.startswith('_'):
                alias_name = '_' + item
                if alias_name in f_cls_attr['__slots__']:
                    item = alias_name
            if original_getattr is not None:
                return original_getattr(self, item)
            else:
                return super(SafeMember, self).__getattribute__(item)

        def init_setattr(self, key, value):
            if not key.startswith('_') and ('_' + key) in f_cls_attr['__slots__']:
                raise AttributeError(f"you can't modify private members:_{key}")
            if original_setattr is not None:
                original_setattr(self, key, value)
            else:
                super(SafeMember, self).__setattr__(key, value)

        f_cls_attr['__getattribute__'] = init_getattr
        f_cls_attr['__setattr__'] = init_setattr

        cls = super().__new__(mcs, f_cls_name, f_cls_parents, f_cls_attr)
        return cls


class SafeMember(metaclass=MetaMemberControl):
    __slots__ = ()

    def __getattribute__(self, item):
        """
        is just for IDE recognize.
        """
        return super().__getattribute__(item)


class ChainMeta(abc.ABCMeta, MetaMemberControl):
    def __new__(cls, name, bases, attr):
        instance = MetaMemberControl.__new__(cls, name, bases, attr)
        instance = abc.ABCMeta.__new__(cls, name, bases, attr)
        return instance


class ABCSafeMember(metaclass=ChainMeta):
    __slots__ = ()

    def __getattribute__(self, item):
        """
        is just for IDE recognize.
        """
        return super().__getattribute__(item)


class ShowTestDescription(TestCase):
    def setUp(self) -> None:
        print('\n' + str(self))
        document = self._testMethodDoc if self._testMethodDoc else None
        print(f"\t{document}") if document else None


class WindowHelper:
    __slots__ = ()

    @staticmethod
    def get_xy_for_move_to_center(screen_w, screen_h, img_w, img_h):
        assert screen_w >= img_w, ValueError('screen_w < img_w')
        assert screen_h >= img_h, ValueError('screen_h < img_h')

        x = (screen_w - img_w) / 2
        y = (screen_h - img_h) / 2
        return x, y


if sys.version_info[0] >= 3 and sys.version_info[1] >= 8:  # py.version >= 3.8
    from Lib.functools import cached_property
else:
    cached_property = property


@contextmanager
def after_end(cb_fun: Callable):
    """
    with after_end(cb_fun) as cb_fun:
        ...

    with after_end(cb_fun=lambda: shutil.rmtree(temp_dir)) as _:  # make sure the temp_dir will remove after finished.
        ...
    """
    try:
        yield cb_fun
    finally:
        cb_fun()
