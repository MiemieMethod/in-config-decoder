from __future__ import annotations

from abc import ABC, abstractmethod
from typing import ClassVar, TYPE_CHECKING

if TYPE_CHECKING:
    from .byte_buf import ByteBuf
    from .data_tag import DataTag, DataTagType

type DataType = bool | int | bytes | str | SerializableObject | list[DataType] | dict[DataType, DataType]

class SerializableObject(ABC):
    NAME: ClassVar[str]
    ID: ClassVar[int]

    def _verify_data_tag(self, tag: DataTag, expected: DataTagType):
        assert tag.type == expected, f"Tag type mismatch, expected {expected} got {tag.type} at member index {tag.member_index}"

    @abstractmethod
    def serialize(self, buf: ByteBuf):
        pass

    @abstractmethod
    def deserialize(self, buf: ByteBuf):
        pass

    @classmethod
    def from_buffer(cls, buf: ByteBuf):
        instance = cls()
        instance.deserialize(buf)
        return instance

    def to_dict(self, decode_strings: bool = False, include_type_name: bool = True) -> dict[DataType, DataType]:
        def process_element(element: DataType) -> dict[DataType, DataType] | list[DataType] | DataType:
            if isinstance(element, SerializableObject):
                return element.to_dict(decode_strings = decode_strings, include_type_name = include_type_name)

            if isinstance(element, list):
                return [process_element(x) for x in element]
            
            if isinstance(element, dict):
                return {key: process_element(value) for (key, value) in element.items()}
            
            if decode_strings and isinstance(element, bytes):
                return element.decode()
            
            return element
        
        value = {key: process_element(value) for (key, value) in self.__dict__.items()}
        if include_type_name:
            value["_type_"] = self.NAME

        return value # type: ignore
