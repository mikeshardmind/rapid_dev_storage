"""
Rapid Dev Storage
~~~~~~~~~~~~~~~~~
A simple devlopment scaffolding tool.
:copyright: (c) 2020 Michael Hall
:license: MIT, see LICENSE for more details.
"""

from ._base_api import Storage, StorageGroup, StoredValue
from ._sqlite_backend import SQLiteBackend
from ._types import NoValue, StorageBackend

__version__ = "0.0.2a"
__title__ = "rapid_dev_storage"
__author__ = "Michael Hall"
__license__ = "MIT"
__copyright__ = "Copyright 2020 Michael Hall"

__all__ = [
    "NoValue",
    "SQLiteBackend",
    "Storage",
    "StorageBackend",
    "StorageGroup",
    "StoredValue",
    "__author__",
    "__copyright__",
    "__license__",
    "__title__",
    "__version__",
]
