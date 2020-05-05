import functools
import keyword

from pathlib import Path
from typing import Union

import apsw
import msgpack

from ._types import AnyStorable, NoValue, StorageBackend, _NoValueType


class SQLiteBackend(StorageBackend):
    def __init__(self, connection, table_name: str, serializer, deserializer):
        self._connection = connection
        self._table_name = table_name
        self._serializer = serializer
        self._deserializer = deserializer

    async def clear_by_keys(self, group_name: str, *keys: str):

        cursor = self._connection.cursor()
        sqlite_args = (group_name,) + keys

        key_len = len(keys)

        # This doesn't insert any user provided values into the formatting and is safe
        # It's a mess, but this is the concession price for what's achieved here.

        match_partial = " AND ".join(f"k{i}=?" for i in range(1, key_len + 1))
        if key_len < 5:
            match_partial += " AND " + " AND ".join(
                f"k{i} IS NULL" for i in range(key_len + 1, 6)
            )

        cursor.execute(
            f"""
            DELETE FROM [ {self._table_name} ]
                WHERE group_name=? AND {match_partial}
            """,
            sqlite_args,
        )

    async def write_data(
        self, group_name: str, *keys: str, value: Union[AnyStorable, _NoValueType]
    ):
        v = self._serializer(value)
        sqlite_args = (group_name,) + keys + (5 - len(keys)) * (None,) + (v,)
        cursor = self._connection.cursor()

        cursor.execute(
            f"""
            INSERT OR REPLACE INTO [ {self._table_name} ]
            (group_name, k1, k2, k3, k4, k5, data)
            VALUES (?,?,?,?,?,?,?)
            """,
            sqlite_args,
        )

    async def get_data(
        self, group_name: str, *keys: str
    ) -> Union[AnyStorable, _NoValueType]:

        cursor = self._connection.cursor()
        sqlite_args = (group_name,) + keys

        key_len = len(keys)

        # This doesn't insert any user provided values into the formatting and is safe
        # It's a mess, but this is the concession price for what's achieved here.

        match_partial = " AND ".join(f"k{i}=?" for i in range(1, key_len + 1))
        if key_len < 5:
            match_partial += " AND " + " AND ".join(
                f"k{i} IS NULL" for i in range(key_len + 1, 6)
            )

        for (data,) in cursor.execute(
            f"""
            SELECT data FROM [ {self._table_name} ]
                WHERE group_name=? AND {match_partial}
            """,
            sqlite_args,
        ):
            return self._deserializer(data)
        return NoValue

    @classmethod
    async def create_backend_instance(
        cls,
        path: Path,
        name: str,
        unique_identifier: int,
        *,
        serializer=None,
        deserializer=None,
    ):

        if not (name.isidentifier() and not keyword.iskeyword(name)):
            raise ValueError(
                "value for parameter name must not be a python keyword "
                "and must be a valid python identifier"
            )

        table_name = f"_{name}-{unique_identifier}"

        con = apsw.Connection(str(path))

        cursor = con.cursor()

        cursor.execute(""" PRAGMA journal_mode="wal" """)

        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS [ {table_name} ] (
                group_name TEXT NOT NULL,
                k1 TEXT,
                k2 TEXT,
                k3 TEXT,
                k4 TEXT,
                k5 TEXT,
                data BLOB,
                PRIMARY KEY (group_name, k1, k2, k3, k4, k5)
            );
            """
        )

        serializer = serializer or msgpack.packb
        deserializer = deserializer or functools.partial(
            msgpack.unpackb, use_list=False
        )

        return cls(con, table_name, serializer, deserializer)
