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
    async def write_data(
        self, group_name: str, *keys: str, value: Union[AnyStorable, _NoValueType],
    ):
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
