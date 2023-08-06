# -*- coding: utf-8 -*-

# Copyright (c) 2020 shmilee

'''
Contains directory raw loader class.
'''

import os

from ..glogger import getGLogger
from ..utils import inherit_docstring
from .base import BaseRawLoader, _raw_copydoc_func

__all__ = ['DirRawLoader']
log = getGLogger('L')


@inherit_docstring((BaseRawLoader,), _raw_copydoc_func, template=None)
class DirRawLoader(BaseRawLoader):
    '''
    Load raw data from a directory. Return a dictionary-like object.

    Attributes
    {Attributes}

    Parameters
    {Parameters}

    Notes
    {Notes}
    3. Directory tree maxdepth is 2.
    '''
    __slots__ = []
    loader_type = 'directory'

    def _special_check_path(self):
        if os.path.isdir(self.path):
            return True
        else:
            log.error("'%s' is not a directory!" % self.path)
            return False

    def _special_open(self):
        return self.path

    def _special_close(self, pathobj):
        pass

    def _special_getkeys(self, pathobj):
        filenames = []
        for _root, _dirs, _files in os.walk(self.path):
            # _root: '/path/'->'', '/path/sub1'->'sub1', '/p/s1/s2'->'s1/s2'
            _root = _root[len(self.path):].strip(os.sep)
            # len(_root) == 0, !find path -maxdepth 1 -type f
            # len(_root)  > 0, maxdepth 2
            # _root.count(os.path.sep) == 1, maxdepth 3
            if len(_root) > 0:
                _dirs[:] = []
            filenames.extend([os.path.join(_root, f) for f in _files])
        return sorted(filenames)

    def _special_get(self, pathobj, key):
        return open(os.path.join(self.path, key))
