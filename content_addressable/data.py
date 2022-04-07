#  Copyright (c) 2022. VMware, Inc.
#  SPDX-License-Identifier: Apache-2.0
from typing import Any, Iterator, Mapping, MutableMapping, Sequence

from content_addressable.core import Content, ContentAddressableError, \
    content_id


class MemoTamperError(ContentAddressableError):
    pass


class Memo(MutableMapping, Content):
    """
    A dictionary that implements the content_addressable Content
    API such that it produces a content identifier
    """

    _content_ids = {}

    def __init__(self, in_data: Mapping = None):
        if in_data is not None:
            for k, v in in_data.items():
                self.__setitem__(k, v)

    def __setitem__(self, k: Any, v: Any) -> None:
        value_id = content_id(v)
        self._content_ids[k] = value_id
        self.__dict__.__setitem__(k, v)

    def __delitem__(self, v: Any) -> None:
        value_id = content_id(v)
        self._content_ids.__delitem__(value_id)
        self.__dict__.__delitem__(v)

    def __getitem__(self, k: Any) -> Any:
        value = self.__dict__.get(k)
        value_id = self._content_ids.get(k)
        if value_id != content_id(value):
            raise MemoTamperError(
                f'value tampering on key: "{k}" value'
                f' does not match content_id: "{value_id}" '
            )
        if hasattr(value, '__copy__'):
            return value.__copy__()
        return value

    def __len__(self) -> int:
        return len(self.__dict__)

    def __iter__(self) -> Iterator[Any]:
        return self.__dict__.__iter__()

    def __copy__(self):
        return self.copy()

    def as_list(self) -> Sequence[Any]:
        return [self.to_data()]

    def to_data(self) -> Mapping[Any, Any]:
        return self.__dict__

    def copy(self) -> 'Memo':
        return Memo.create(self.__dict__)

    @classmethod
    def create(cls, in_data: Mapping = None):
        if in_data is None:
            in_data = {}
        out = Memo()
        for k, v in in_data.items():
            out[k] = v
        return out
