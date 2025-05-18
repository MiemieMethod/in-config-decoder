from __future__ import annotations

import os

from typing import Literal, TYPE_CHECKING

from .byte_buf import ByteBuf
from .type_registry import TypeRegistry

if TYPE_CHECKING:
    from .serializable_object import SerializableObject

type ValueType = bool | int | str | float | dict[ValueType, ValueType] | list[ValueType] | SerializableObject | None

class ConfigTable:
    name: str

    _filename: str
    _value_type: str
    _mode: str

    _registry: TypeRegistry

    _key_to_offset: dict[ValueType, int | dict[ValueType, int]]
    _list_begin_offsets: dict[int, dict[ValueType, int]]
    _tmap_offsets: dict[ValueType, int | dict[ValueType, int]]

    _extra_find_layer: int
    _extra_list_tag: int
    _extra_list_begin_offset: int

    _cached_value: None | SerializableObject | dict[ValueType, SerializableObject] | dict[ValueType, dict[ValueType, SerializableObject]]

    def __init__(self, name: str, file_name: str, value_type: str, mode: Literal["one", "map", "bmap"], registry: TypeRegistry) -> None:
        self.name = name

        self._filename = file_name
        self._value_type = value_type
        self._mode = mode

        self._registry = registry

        self._key_to_offset = {}
        self._list_begin_offsets = {}
        self._tmap_offsets = {}

        self._extra_find_layer = 0
        self._extra_list_tag = 0
        self._extra_list_begin_offset = 0

        self._cached_value = None

    def _read_type(self, data: ByteBuf, type: int, use_unreal_serialization: bool = False) -> ValueType:
        match type:
            case 1:
                return data.read_bool() if not use_unreal_serialization else bool(data.read_fixed_int())
            case 2:
                return data.read_byte()
            case 3:
                return data.read_short() if not use_unreal_serialization else data.read_fixed_short()
            case 4:
                return data.read_fixed_short()
            case 5:
                return data.read_int() if not use_unreal_serialization else data.read_fixed_int()
            case 6:
                return data.read_fixed_int()
            case 7:
                return data.read_long() if not use_unreal_serialization else data.read_fixed_long()
            case 8:
                return data.read_fixed_long()
            case 9:
                return data.read_float()
            case 10:
                return data.read_double()
            case 11:
                if use_unreal_serialization:
                    size = data.read_fixed_int()
                    if 0 > size:
                        return data._fp.read(2 * -size)[:-2].decode("utf-16le")

                    return data._fp.read(size)[:-1].decode()

                return data.read_bytes().decode()
            case _:
                assert False, f"Tried to read invalid type {type} in config table {self.name}"

    def load_one[T: SerializableObject](self, base_directory: str) -> T: # type: ignore
        return self._mode_checked_load(base_directory, "one") # type: ignore
    
    def load_map[TValueType: ValueType, TEntry: SerializableObject](self, base_directory: str) -> dict[TValueType, TEntry]: # type: ignore
        return self._mode_checked_load(base_directory, "map") # type: ignore
    
    def load_bmap[TKey: ValueType, TSubKey: ValueType, TEntry: SerializableObject](self, base_directory: str) -> dict[TKey, dict[TSubKey, TEntry]]: # type: ignore
        return self._mode_checked_load(base_directory, "bmap") # type: ignore

    def _mode_checked_load(self, base_directory: str, mode: str):
        if mode != self._mode:
            raise ValueError(f"cannot load table of type {self._mode} as {mode}.")
        
        return self.load(base_directory)

    def load(self, base_directory: str) -> SerializableObject | dict[ValueType, SerializableObject] | dict[ValueType, dict[ValueType, SerializableObject]]:
        if self._cached_value is not None:
            return self._cached_value
        
        data_path = os.path.join(base_directory, self._filename)
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"{data_path} does not exist.")
    
        value_type = self._registry.get_by_name(self._value_type)
        if self._mode == "one":
            data = ByteBuf.from_file(data_path)
            entry_count = data.read_int()
            assert entry_count, f"Config table with one element had entry_count != 1, {entry_count}"
            
            object = value_type.from_buffer(data)
            assert not data.has_data(), "Did not read entire config table with one element"
            return object
        
        extra = ByteBuf.from_file(data_path + "extra")
        self._load_extra_data(extra)

        if os.path.exists(data_path + "tmap"):
            tmap = ByteBuf.from_file(data_path + "tmap")
            self._load_tmap_data(tmap)

        data = ByteBuf.from_file(data_path)

        values = {}
        for key, value in self._key_to_offset.items():
            if isinstance(value, dict):
                subvalues = {}
                for subkey, offset in value.items():
                    data._fp.seek(offset)
                    subvalues[subkey] = value_type.from_buffer(data)

                values[key] = subvalues
            else:
                data._fp.seek(value)
                values[key] = value_type.from_buffer(data)

        self._cached_value = values
        return values
    
    def _load_extra_data(self, extra: ByteBuf):
        def read_child_offsets():
            while extra.read_byte() > 0:
                begin_offset = extra.read_int()
                child_type = extra.read_byte()
                child_size = extra.read_int()

                self._list_begin_offsets[begin_offset] = {}
                for _ in range(child_size):
                    child_row_begin = extra.read_int()
                    child_key = self._read_type(extra, child_type)

                    self._list_begin_offsets[begin_offset][child_key] = child_row_begin
                    read_child_offsets()

        entry_type = extra.read_byte()
        self._extra_find_layer = extra.read_byte()

        self._extra_list_tag = extra.read_byte()
        self._extra_list_begin_offset = extra.read_int()
        list_size = extra.read_int()

        for _ in range(list_size):
            row_begin = extra.read_int()

            match self._mode:
                case "map":
                    key_value = self._read_type(extra, entry_type)

                    self._key_to_offset[key_value] = row_begin
                    read_child_offsets()

                case "bmap":
                    key_value = self._read_type(extra, entry_type >> 4)
                    key_2_value = self._read_type(extra, entry_type & 0xf)

                    if key_value not in self._key_to_offset:
                        self._key_to_offset[key_value] = {}

                    self._key_to_offset[key_value][key_2_value] = row_begin # type: ignore
                    read_child_offsets()

        assert extra.read_byte() == 0

    def _load_tmap_data(self, tmap: ByteBuf):
        # this is read in an unreal c++ class, not in lua, so the serialization is slightly different
        key_type = tmap.read_fixed_int()
        subkey_type = tmap.read_fixed_int()
        entry_count = tmap.read_fixed_int()

        for _ in range(entry_count):
            key = self._read_type(tmap, key_type, use_unreal_serialization = True)
            if subkey_type != 0:
                value: int | dict[ValueType, int] = {}
                subkey_count = tmap.read_fixed_int()
                for _ in range(subkey_count):
                    subkey = self._read_type(tmap, subkey_type, use_unreal_serialization = True)
                    offset = tmap.read_fixed_int()
                    value[subkey] = offset
            else:
                value = tmap.read_fixed_int()

            self._tmap_offsets[key] = value
        
        assert not tmap.has_data()