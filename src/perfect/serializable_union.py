from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from .serializable_object import SerializableObject

if TYPE_CHECKING:
    from .byte_buf import ByteBuf
    from .type_registry import TypeRegistry

class SerializableUnion(SerializableObject):
    UNION: ClassVar[list[str]]
    REGISTRY: ClassVar[TypeRegistry]

    value: SerializableObject | None

    def serialize(self, buf: ByteBuf):
        if self.value is None:
            buf.write_int(0)
            return
        
        buf.write_int(self.value.ID)
        buf.write_object(self.value)

    def deserialize(self, buf: ByteBuf):
        id = buf.read_int()
        if id == 0:
            self.value = None
            return
        
        value_type = self.REGISTRY.get_by_id(id)
        assert value_type.NAME in self.UNION, f"Got unsupported union type {value_type.NAME} by ID lookup {id}"
        self.value = value_type.from_buffer(buf)

    def to_dict(self, decode_strings: bool = False, include_type_name: bool = True):
        return self.value.to_dict(decode_strings = decode_strings, include_type_name = include_type_name) if self.value else None