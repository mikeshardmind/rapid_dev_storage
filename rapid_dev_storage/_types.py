from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Union

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
    async def get_all_by_group(self, group_name: str):
        """ Concrete implmentations must yield a 2-tuple of (key tuple, value) """
        ...

    @abstractmethod
    async def get_all_by_key_prefix(self, group_name: str, *keys: str):
        """ Concrete implementations must yield a 2-tuple of (key tuple, value) """
        ...
