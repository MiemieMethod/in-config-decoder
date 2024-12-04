from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .serializable_object import SerializableObject

class TypeRegistry:
    _class_id_map: dict[int, type[SerializableObject]]
    _class_name_map: dict[str, type[SerializableObject]]

    def __init__(self) -> None:
        self._class_id_map = {}
        self._class_name_map = {}

    def register_class(self, clazz: type[SerializableObject]):
        self._class_name_map[clazz.NAME] = clazz
        if clazz.ID != 0:
            self._class_id_map[clazz.ID] = clazz

    def get_by_id(self, id: int) -> type[SerializableObject]:
        if id == 0:
            raise RuntimeError("Looking up a type with ID 0 is not supported.")
        
        return self._class_id_map[id]
    
    def get_by_name(self, name: str) -> type[SerializableObject]:
        return self._class_name_map[name]