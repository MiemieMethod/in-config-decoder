from __future__ import annotations

import struct

from io import BytesIO
from typing import Callable, ClassVar

from .vector import Vector2, Vector3, Vector4
from .data_tag import DataTag, DataTagType
from .serializable_object import SerializableObject

class ByteBuf:
    enable_tag_skipping: ClassVar[bool] = False

    _fp: BytesIO
    _size: int

    def __init__(self, data: bytes | None = None) -> None:
        self._fp = BytesIO(data) if data else BytesIO()
        self._size = len(data) if data else 0

    @classmethod
    def from_file(cls, file: str):
        with open(file, "rb") as f:
            return cls(f.read())

    def read_byte(self) -> int:
        return int.from_bytes(self._fp.read(1))
    
    def read_bool(self):
        return self.read_byte() != 0
    
    def _read_compressed_unsigned(self, max_count: int) -> int:
        first = self.read_byte()
        if not (first & 0x80):
            return first

        if first == 0xff:
            return int.from_bytes(self._fp.read(max_count), "little", signed=False)
        
        first_byte_mask = 0b01111111
        first_byte_shift = 0

        cond_var = first

        value = 0
        while (cond_var & 0x80) and max_count >= 0:
            cond_var <<= 1
            max_count -= 1

            value <<= 8
            value |= self.read_byte()

            first_byte_mask >>= 1
            first_byte_shift += 8

        value |= (first & first_byte_mask) << first_byte_shift
        assert max_count >= 0, "Invalid compressed integer"
        return value
    
    def read_short(self) -> int:
        return self._read_compressed_unsigned(2)
    
    def read_int(self):
        value = self._read_compressed_unsigned(4)
        if value > 0x80000000:
            value = int.from_bytes(value.to_bytes(4), signed=True)
        
        return value
    
    def read_long(self) -> int:
        return self._read_compressed_unsigned(8)
    
    def read_net_header(self) -> int:
        return int.from_bytes(self._fp.read(4), "big")
    
    def read_float(self) -> float:
        return struct.unpack("f", self._fp.read(4))[0]
    
    def read_double(self) -> float:
        return struct.unpack("d", self._fp.read(8))[0]
    
    def read_bytes(self) -> bytes:
        size = self.read_int()
        return self._fp.read(size)
    
    def read_vector2(self) -> Vector2:
        return Vector2(self.read_float(), self.read_float())
    
    def read_vector3(self) -> Vector3:
        return Vector3(self.read_float(), self.read_float(), self.read_float())
    
    def read_vector4(self) -> Vector4:
        return Vector4(self.read_float(), self.read_float(), self.read_float(), self.read_float())
    
    def read_data_tag(self) -> DataTag:
        assert self.has_data()
        return DataTag.from_value(self.read_short())
    
    def read_fixed_short(self) -> int:
        return int.from_bytes(self._fp.read(2), "little", signed = True)

    def read_fixed_int(self) -> int:
        return int.from_bytes(self._fp.read(4), "little", signed = True)
    
    def read_fixed_long(self) -> int:
        return int.from_bytes(self._fp.read(8), "little", signed = True)
    
    def read_object_tags(self):
        while (tag := self.read_data_tag()).type != DataTagType.END_OBJECT:
            yield tag
    
    def read_object[TObject: SerializableObject](self, clazz: type[TObject], read_size: bool = True) -> TObject:
        data = ByteBuf(self.read_bytes()) if read_size else self
        value = clazz.from_buffer(data)
        if read_size:
            assert not data.has_data(), f"Did not read entire buffer when reading object of type {clazz}"

        return value
    
    def read_array[TValue](self, read_func: Callable[[ByteBuf], TValue], read_tag: bool = True) -> list[TValue]:
        arr = []

        if read_tag:
            data = ByteBuf(self.read_bytes())
            while data.has_data():
                data.read_data_tag() # value_tag
                arr.append(read_func(data))
        else:
            for _ in range(self.read_int()):
                arr.append(read_func(self))

        return arr
    
    def read_dict[TKey, TValue](self, key_func: Callable[[ByteBuf], TKey], value_func: Callable[[ByteBuf], TValue], read_tag: bool = True) -> dict[TKey, TValue]:
        dict = {}

        if read_tag:
            data = ByteBuf(self.read_bytes())
            while data.has_data():
                data.read_data_tag() # key_tag
                key = key_func(data)
                data.read_data_tag() # value_tag
                value = value_func(data)
                dict[key] = value
        else:
            for _ in range(self.read_int()):
                key = key_func(self)
                value = value_func(self)
                dict[key] = value
        
        return dict
    
    def read_nullable[TValue](self, read_func: Callable[[ByteBuf], TValue]) -> TValue | None:
        if self.read_bool():
            return read_func(self)
    
        return None
    
    # write methods

    def write_byte(self, value: int):
        self._fp.write(value.to_bytes(1))

    def _write_compressed_unsigned(self, max_count: int, value: int):
        if 0 > value:
            value = int.from_bytes(value.to_bytes(8), signed = False)
        
        if   value < (1 << 7):
            self.write_byte(value)
        elif value < (1 << 14):
            self.write_byte((value >> 8) | 0b10000000)
            self.write_byte(value & 0xff)
        elif value < (1 << 21):
            self.write_byte((value >> 16) | 0b11000000)
            self.write_byte((value >> 8) & 0xff)
            self.write_byte(value & 0xff)
        elif value < (1 << 28):
            self.write_byte((value >> 24) | 0b11100000)
            self.write_byte((value >> 16) & 0xff)
            self.write_byte((value >> 8) & 0xff)
            self.write_byte(value & 0xff)
        elif value < (1 << 35):
            self.write_byte((value >> 32) | 0b11110000)
            self.write_byte((value >> 24) & 0xff)
            self.write_byte((value >> 16) & 0xff)
            self.write_byte((value >> 8) & 0xff)
            self.write_byte(value & 0xff)
        elif value < (1 << 42):
            assert max_count > 4, "compressed int too small"
            self.write_byte((value >> 40) | 0b11111000)
            self.write_byte((value >> 32) & 0xff)
            self.write_byte((value >> 24) & 0xff)
            self.write_byte((value >> 16) & 0xff)
            self.write_byte((value >> 8) & 0xff)
            self.write_byte(value & 0xff)
        elif value < (1 << 45):
            assert max_count > 4, "compressed int too small"
            self.write_byte((value >> 48) | 0b11111100)
            self.write_byte((value >> 40) & 0xff)
            self.write_byte((value >> 32) & 0xff)
            self.write_byte((value >> 24) & 0xff)
            self.write_byte((value >> 16) & 0xff)
            self.write_byte((value >> 8) & 0xff)
            self.write_byte(value & 0xff)
        elif value < (1 << 56):
            assert max_count > 4, "compressed int too small"
            self.write_byte(0b11111110)
            self.write_byte((value >> 48) & 0xff)
            self.write_byte((value >> 40) & 0xff)
            self.write_byte((value >> 32) & 0xff)
            self.write_byte((value >> 24) & 0xff)
            self.write_byte((value >> 16) & 0xff)
            self.write_byte((value >> 8) & 0xff)
            self.write_byte(value & 0xff)
        else:
            assert max_count > 4, "compressed int too small"
            self.write_byte(0b11111111)
            self._fp.write(value.to_bytes(8, "little"))

    def write_bool(self, value: bool):
        self.write_byte(1 if value else 0)

    def write_short(self, value: int):
        self._write_compressed_unsigned(2, value)

    def write_int(self, value: int):
        self._write_compressed_unsigned(4, value)

    def write_long(self, value: int):
        self._write_compressed_unsigned(8, value)
    
    def write_net_header(self, value: int):
        self._fp.write(value.to_bytes(4, "big"))

    def write_float(self, value: float):
        self._fp.write(struct.pack("f", value))

    def write_double(self, value: float):
        self._fp.write(struct.pack("d", value))

    def write_bytes(self, value: bytes):
        self.write_int(len(value))
        if len(value) > 0:
            self._fp.write(value)

    def write_vector2(self, value: Vector2):
        self.write_float(value.x)
        self.write_float(value.y)

    def write_vector3(self, value: Vector3):
        self.write_float(value.x)
        self.write_float(value.y)
        self.write_float(value.z)

    def write_vector4(self, value: Vector4):
        self.write_float(value.x)
        self.write_float(value.y)
        self.write_float(value.z)
        self.write_float(value.w)

    def write_data_tag(self, value: DataTag):
        self.write_short(value.to_value())

    def write_object(self, obj: SerializableObject, write_size: bool = True):
        if not write_size:
            obj.serialize(self)
        else:
            buf = ByteBuf()
            obj.serialize(buf)
            self.write_bytes(buf.get_buffer())

    def write_array[TValue](self, type: DataTagType, value: list[TValue], write_func: Callable[[ByteBuf, TValue], None], write_tag: bool = True):
        if not write_tag:
            self.write_int(len(value))
            for element in value:
                write_func(self, element)
        else:
            buf = ByteBuf()
            key_tag = DataTag(0, type)
            for element in value:
                buf.write_data_tag(key_tag)
                write_func(buf, element)

            self.write_bytes(buf.get_buffer())

    def write_dict[TKey, TValue](self, key_type: DataTagType, value_type: DataTagType, value: dict[TKey, TValue], 
                   key_func: Callable[[ByteBuf, TKey], None],
                   value_func: Callable[[ByteBuf, TValue], None],
                   write_tag: bool = True):
        if not write_tag:
            self.write_int(len(value))
            for key, element in value.items():
                key_func(self, key)
                value_func(self, element)
        else:
            buf = ByteBuf()
            key_tag = DataTag(0, key_type)
            value_tag = DataTag(0, value_type)
            for key, element in value.items():
                buf.write_data_tag(key_tag)
                key_func(buf, key)
                buf.write_data_tag(value_tag)
                value_func(buf, element)
            
            self.write_bytes(buf.get_buffer())

    def write_nullable[TValue](self, value: TValue | None, write_func: Callable[[ByteBuf, TValue], None]):
        if value is not None:
            self.write_bool(True)
            write_func(self, value)
        else:
            self.write_bool(False)

    def has_data(self) -> bool:
        return self._fp.tell() != self._size

    def get_buffer(self) -> bytes:
        return self._fp.getvalue()
    
    def skip_value(self, tag: DataTag):
        match tag.type:
            case DataTagType.BOOL:
                val = self.read_bool()
            case DataTagType.SHORT:
                val = self.read_short()
            case DataTagType.INT:
                val = self.read_int()
            case DataTagType.LONG:
                val = self.read_long()
            case DataTagType.FLOAT:
                val = self.read_float()
            case DataTagType.DOUBLE:
                val = self.read_double()
            case DataTagType.VECTOR3:
                val = self.read_vector3()
            case DataTagType.VECTOR4:
                val = self.read_vector4()
            case DataTagType.COMPLEX:
                val = self.read_bytes()
            case DataTagType.STRING:
                val = self.read_bytes()
            case _:
                val = None
                assert False, tag

        if not ByteBuf.enable_tag_skipping:
            raise RuntimeError(f"Tried to skip tag {tag} with value: {val}")