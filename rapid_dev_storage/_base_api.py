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

from typing import Awaitable, Union

from ._types import AnyStorable, StorageBackend, _NoValueType


class StoredValue:
    def __init__(self, backend: StorageBackend, group_name: str, *keys: str):
        self._backend = backend
        self._keys = keys
        self._group_name = group_name

    def set_value(self, value: AnyStorable) -> Awaitable[None]:
        """
        Sets a value
        """
        return self._backend.write_data(self._group_name, *self._keys, value=value)

    def get_value(self) -> Awaitable[Union[AnyStorable, _NoValueType]]:
        """
        Gets a value

        May also return ``rapid_dev_storage.NoValue``
        if there is not a value.
        The abscence of a value is distinct from storing ``None``
        Instances of subclasses of Storage may optionally fill in defaults
        by replacing this class and it's use.
        """
        return self._backend.get_data(self._group_name, *self._keys)

    def clear_value(self) -> Awaitable[None]:
        """ Clears a Value """
        return self._backend.clear_by_keys(self._group_name, *self._keys)


class StorageGroup:
    def __init__(self, backend: StorageBackend, group_name: str):
        self._backend = backend
        self._group_name = group_name

    def __getitem__(self, keys):
        """
        The key value restriction is an implementation detail of the included
        SQLiteBackend class.
        I suggest retaining it, but this can also be replaced.
        """
        if len(keys) > 5:
            raise ValueError("Must not provide more than a 5-part key")
        return StoredValue(self._backend, self._group_name, *keys)

    def clear_group(self) -> Awaitable[None]:
        """ Clears an entire group """
        return self._backend.clear_group(self._group_name)

    async def all_items(self):
        """
        Iterates over all items stored in the group

        The data is yielded as a 2-tuple consisting of the tuple key,
        and the value which was associated
        """
        async for key, value in self._backend.get_all_by_group(self._group_name):
            yield key, value


class Storage:
    """
    This is the basic storage wrapper class.

    It can be extended with additional functionality
    and adapters for specific data types, as well as adding
    facotry methods for instantiation including the required backend
    """

    def __init__(self, backend: StorageBackend):
        self._state = None
        self._backend = backend

    def get_group(self, name: str):
        return StorageGroup(self._backend, name)
