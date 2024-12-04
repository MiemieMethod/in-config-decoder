from __future__ import annotations

from enum import Enum
from typing import NamedTuple

class DataTagType(Enum):
    END_OBJECT = 1
    BOOL = 2
    SHORT = 3
    INT = 4
    LONG = 5
    #FLOAT16 = 6 # unused
    FLOAT = 7
    DOUBLE = 8
    VECTOR2 = 8 # aliasing is intentional, sadly
    VECTOR3 = 9
    VECTOR4 = 10
    COMPLEX = 11 # object, list, dict
    #COMPLEX2 = 12 unused
    STRING = 13 # same format as COMPLEX

class DataTag(NamedTuple):
    member_index: int
    type: DataTagType

    @staticmethod
    def from_value(value: int) -> DataTag:
        type = value & 0xf
        index = value >> 4
        return DataTag(index, DataTagType(type))
    
    def to_value(self) -> int:
        return self.member_index << 4 | self.type.value