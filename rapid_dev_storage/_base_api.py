from typing import Awaitable, Union

from ._types import AnyStorable, StorageBackend, _NoValueType


class StoredValue:
    def __init__(self, backend: StorageBackend, group_name: str, *keys: str):
        self._backend = backend
        self._keys = keys
        self._group_name = group_name

    def set_value(self, value: AnyStorable) -> Awaitable[None]:
        return self._backend.write_data(value, self._group_name, *self._keys)

    def get_value(self) -> Awaitable[Union[AnyStorable, _NoValueType]]:
        return self._backend.get_data(self._group_name, *self._keys)

    def clear_value(self) -> Awaitable[None]:
        return self._backend.clear_by_keys(self._group_name, *self._keys)


class StorageGroup:
    def __init__(self, backend: StorageBackend, group_name: str):
        self._backend = backend
        self._group_name = group_name

    def __getitem__(self, keys):
        if len(keys) > 5:
            raise ValueError("Must not provide more than a 5-part key")
        return StoredValue(self._backend, self._group_name, *keys)


class Storage:
    def __init__(self, backend: StorageBackend):
        self._state = None
        self._backend = backend

    def get_group(self, name: str):
        return StorageGroup(self._backend, name)
