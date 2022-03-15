#
# Copyright 2008,2009 Free Software Foundation, Inc.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

# The presence of this file turns this directory into a Python package

'''
This is the GNU Radio LACROSSE module. Place your Python package
description here (python/__init__.py).
'''
import os

# import pybind11 generated symbols into the lacrosse namespace
try:
    # this might fail if the module is python-only
    from .lacrosse_python import *
except ModuleNotFoundError:
    pass

from .TX29U import TX29U
# import any pure python here
#
