# -*- coding: utf-8 -*-

# Copyright (c) 2020 shmilee

'''
'''

import os
import importlib

from ..__about__ import __ENABLE_USERBASE__, __userbase__
from .processor import Processor, plog
from .multiprocessor import MultiProcessor

__all__ = ['Processor_Lib', 'Processor_Names', 'Processor_Alias',
           'register_Processor', 'register_user_Processors', 'find_Processor']

Processor_Lib = {}
Processor_Names = []
Processor_Alias = {}


def register_Processor(name, mod_path, alias=None):
    '''
    Add processor *name* module and its alias in *Processor_Lib*.
    Processor_Lib[name] = (mod_path, {class_cache_dict})
    *mod_path* can be relative to `processors` package.
    '''
    if name in Processor_Lib:
        plog.warning("Processor %s is already in Processor_Lib!" % name)
    else:
        Processor_Lib[name] = (mod_path, {})
        # update names
        Processor_Names.append(name)
        Processor_Names.sort()
        if alias:
            if alias in Processor_Alias:
                plog.warning("Alias, %s: %s -> %s: %s " % (
                    alias, Processor_Alias[alias], alias, name))
            Processor_Alias[alias] = name


# GTC Processors
register_Processor('GTCv3', '..GTCv3', 'G3')
register_Processor('GTCv4', '..GTCv4', 'G4')


def register_user_Processors(dirname):
    '''
    Rgister user defined Processors from *dirname* in __userbase__.

    Notes
    -----
    1. default dirname = 'user_processors'
    2. Processor name is the directory name in *dirname*.
    3. Add '__init__.py' in every directory.
    4. Write alias name in 'alias' file in the directory if needed.
    '''
    _user_path = os.path.join(__userbase__, dirname)
    if not os.path.isdir(_user_path):
        return
    for dname in os.listdir(_user_path):
        init_py = os.path.join(_user_path, dname, '__init__.py')
        alias_f = os.path.join(_user_path, dname, 'alias')
        if os.path.isfile(init_py):
            mod_path = '%s.%s' % (dirname, dname)
            alias = None
            if os.path.isfile(alias_f):
                with open(alias_f, 'r') as f:
                    alias = f.readline().strip()
            register_Processor(dname, mod_path, alias=alias)


if __ENABLE_USERBASE__:
    register_user_Processors('user_processors')


def find_Processor(name, parallel):
    '''Return Processor class of *name*'''
    mod_path, class_cache = Processor_Lib.get(name)
    if parallel in class_cache:
        gdpcls = class_cache[parallel]
    else:
        if mod_path.startswith('.'):
            pkg = '.'.join(__name__.split('.')[:-1])  # rm .lib
            plog.debug('Importing %s relative to %s ...' % (mod_path, pkg))
            ppack = importlib.import_module(mod_path, package=pkg)
        else:
            ppack = importlib.import_module(mod_path)
        # get Base
        base = getattr(ppack, 'Base_%s' % name)
        # which one
        if parallel == 'off':
            gdpcls = type(name, (base, Processor), {'__slots__': []})
            globals()[name] = gdpcls
        elif parallel == 'multiprocess':
            gdpcls = type('Multi%s' % name, (base, MultiProcessor),
                          {'__slots__': []})
            # cache in module scope, useful when multiprocessing
            globals()['Multi%s' % name] = gdpcls
        elif parallel == 'mpi4py':
            raise ValueError('TODO %s' % parallel)
        else:
            raise ValueError('Unsupported parallel-lib: %s' % parallel)
        plog.debug("'lib' scope's global variables: %s" % globals().keys())
        # cache in Processor_Lib
        Processor_Lib[name][1][parallel] = gdpcls
    return gdpcls
