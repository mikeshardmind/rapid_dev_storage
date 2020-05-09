"""
MIT License

Copyright (c) 2020 Michael Hall

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, AsyncIterator, Dict, List, Tuple, Union

AnyStorable = Union[Dict[str, Any], List[Any], int, float, str, None]


class _NoValueType:
    """
    Represents when there is no data.
    This is distinct from storing a value of None
    """

    def __bool__(self):
        return False


NoValue = _NoValueType()


class StorageBackend(ABC):
    """
    This abstract base class shows the interfaces
    required to use a class as a replacement backend for the included ones

    Interfaces here are async to allow dropping
    in other interfaces which would strictly need to be async
    """

    @abstractmethod
    async def write_data(self, group_name: str, *keys: str, value: AnyStorable):
        ...

    @abstractmethod
    async def get_data(
        self, group_name: str, *keys: str
    ) -> Union[AnyStorable, _NoValueType]:
        ...

    @classmethod
    @abstractmethod
    async def create_backend_instance(
        cls,
        path: Path,
        name: str,
        unique_identifier: int,
        *,
        serializer=None,
        deserializer=None,
    ):
        ...

    @abstractmethod
    async def clear_by_keys(self, group_name: str, *keys: str):
        ...

    @abstractmethod
    async def clear_group(self, group_name: str):
        ...

    @abstractmethod
    async def clear_by_key_prefix(self, group_name: str, *keys: str):
        ...

    @abstractmethod
    def get_all_by_group(
        self, group_name: str
    ) -> AsyncIterator[Tuple[Tuple[str, ...], AnyStorable]]:
        """ Concrete implmentations must asynchronously yield a 2-tuple of (key tuple, value) """
        ...

    @abstractmethod
    def get_all_by_key_prefix(
        self, group_name: str, *keys: str
    ) -> AsyncIterator[Tuple[Tuple[str, ...], AnyStorable]]:
        """ Concrete implementations must asynchronously yield a 2-tuple of (key tuple, value) """
        ...
