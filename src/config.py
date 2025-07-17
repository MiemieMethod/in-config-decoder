import json
import os
import re

from lupa.lua54 import LuaRuntime, LUA_MAXINTEGER
from .perfect import *

def read_long_modified(buf):
    read = ByteBuf._read_compressed_unsigned(buf, 8)
    if read > LUA_MAXINTEGER:
        return 'long_int_indicator.' + str(read)
    else:
        return read

def read_string(buf):
    return ByteBuf.read_bytes(buf).decode('utf-8')

methods = {
    'readBool': ByteBuf.read_bool,
    'readByte': ByteBuf.read_byte,
    'readShort': ByteBuf.read_short,
    'readFshort': ByteBuf.read_short, # todo
    'readInt': ByteBuf.read_int,
    'readFint': ByteBuf.read_int, # todo
    'readLong': read_long_modified,
    'readFlong': read_long_modified, # todo
    'readFloat': ByteBuf.read_float,
    'readDouble': ByteBuf.read_double,
    'readSize': ByteBuf.read_int,
    'readString': read_string,
    'GetEBuf': None,
}

def decode_configs(I_N_CORE_DATA_PATH, is_repo = False, version = ''):
    with open(os.path.join("cfg/script/GenV2", version, "Cfg/CfgTypes.lua")) as f:
        lua = LuaRuntime(unpack_returned_tuples=True)
        config = lua.execute(f.read().replace('local UENewTable = _ENV.UENewTable', 'function UENewTable(size, value)\n\
            local t = {}\n\
            rawset(t, "_type", "dict")\n\
            return t\n\
        end\n\
        function UENewList(size, value)\n\
            local t = {}\n\
            rawset(t, "_type", "list")\n\
            return t\n\
        end').replace('list = UENewTable', 'list = UENewList').replace('local map = {}', ''))

    init_function = config.InitTypes

    init_data = init_function(methods)

    name_to_bean_map = {}
    bean_orders = {}
    for i in init_data.beans:
        bean = init_data.beans[i]
        name_to_bean_map[bean._name] = bean
        bean_orders[bean._name] = {}
        if bean._name2number:
            for field in bean._name2number:
                bean_orders[bean._name][bean._name2number[field]] = field

    registry = TypeRegistry()

    for i in init_data.beans:
        bean = init_data.beans[i]
        _name = bean._name
        _id = bean._id

        def create_bean_object_class(name, id, bean):
            class BeanObject(SerializableObject):
                NAME = name
                ID = id

                def __init__(self):
                    self.cache = None

                def serialize(self, buf: ByteBuf):
                    pass

                def deserialize(self, buf: ByteBuf):
                    parsed = bean._deserialize(buf)
                    self.cache = self.parse(parsed)
                    # print(self.cache)

                def parse(self, luaTable):
                    luatable_type = type(luaTable)

                    def parseLuatable(built, key, luaTable):
                        if isinstance(luaTable, luatable_type):
                            built[key] = self.parse(luaTable)
                        elif isinstance(luaTable, str) and luaTable.startswith('long_int_indicator.'):
                            built[key] = int(luaTable.split('.')[1])
                        else:
                            built[key] = luaTable

                    def parseSpecialLuaTbale(luaTable):
                        # table = None
                        if luaTable._type == 'list':
                            table = []
                        elif luaTable._type == 'dict':
                            table = {}
                        else:
                            table = {}
                            # print(f'Unknown luaTable type {luaTable._type}')
                        if isinstance(table, list):
                            for i in luaTable:
                                if i == '_type':
                                    continue
                                table.append(luaTable[i])
                                parseLuatable(table, i - 1, luaTable[i])
                        elif isinstance(table, dict):
                            to_sort = []
                            for i in luaTable:
                                if i == '_type':
                                    continue
                                to_sort.append(i)
                            for i in sorted(to_sort):
                                parseLuatable(table, i, luaTable[i])
                        return table

                    name = luaTable._name
                    # print(name)
                    this_bean = name_to_bean_map.get(name)
                    if this_bean is None:
                        if hasattr(luaTable, '_type'):
                            return parseSpecialLuaTbale(luaTable)
                        else:
                            print(f'Bean {name} not found')
                    orders = bean_orders[name]
                    built = {
                        '_name': name,
                        '_id': luaTable._id
                    }
                    for order in sorted(orders):
                        parseLuatable(built, orders[order], luaTable[orders[order]])
                    # print(built)
                    return built


            return BeanObject


        BeanObjectClass = create_bean_object_class(_name, _id, bean)
        registry.register_class(BeanObjectClass)


    for i in init_data.tables:
        table = init_data.tables[i]
        config_table = ConfigTable(
            name=table.name,
            file_name=table.file,
            value_type=table.value_type,
            mode=table.mode,
            registry=registry
        )
        print('Loading', table.file)
        loaded_table = config_table.load(os.path.join(I_N_CORE_DATA_PATH, r'X6Game/Content/config_output'))
        # print(loaded_table)

        if table.mode == 'map':
            for key, value in loaded_table.items():
                loaded_table[key] = value.cache
        elif table.mode == 'bmap':
            for key, value in loaded_table.items():
                for k, v in value.items():
                    loaded_table[key][k] = v.cache
        elif table.mode == 'one':
            loaded_table = loaded_table.cache

        if is_repo:
            os.makedirs('cfg/repo/ConfigOutput/', exist_ok=True)
            with open(f'cfg/repo/ConfigOutput/{table.file.replace(".bin", ".json")}', 'w', encoding='utf-8') as f:
                json.dump(loaded_table, f, ensure_ascii=False, indent=2)
        else:
            os.makedirs(f'cfg/config_output/{table.value_type.split(".")[0]}', exist_ok=True)
            with open(f'cfg/config_output/{table.file.replace(".bin", ".json").replace(".", "/", 1)}', 'w', encoding='utf-8') as f:
                json.dump(loaded_table, f, ensure_ascii=False, indent=2)


def decode_helper(I_N_CORE_DATA_PATH, version = ''):
    def replace_enum_string(s):
        pattern = r'PaperEnum\.Cfg\.(\w+\.\w+)\.(\w+)'
        result = re.sub(pattern, r'enums["\1"].\2', s)
        return result

    with open(os.path.join("cfg/script/GenV2", version, "Cfg/CfgTypes.lua")) as f:
        lua = LuaRuntime(unpack_returned_tuples=True)
        config = lua.execute(f.read().replace('local UENewTable = _ENV.UENewTable', 'function UENewTable(size, value)\n\
        local t = {}\n\
        rawset(t, "_type", "dict")\n\
        return t\n\
    end\n\
    function UENewList(size, value)\n\
        local t = {}\n\
        rawset(t, "_type", "list")\n\
        return t\n\
    end').replace('list = UENewTable', 'list = UENewList').replace('local map = {}', ''))

    init_function = config.InitTypes

    init_data = init_function(methods)

    with open("cfg/enums.json", "w", encoding="utf-8") as f:
        result = {}
        temp = {}
        for i in init_data.enums:
            enum = init_data.enums[i]
            reverse_map = {}
            enum_map = {}
            for j, value in enum.items():
                reverse_map[value] = j
            for j in sorted(reverse_map):
                enum_map[reverse_map[j]] = j
            temp[i] = enum_map
        for i in sorted(temp):
            result[i] = temp[i]
        json.dump(result, f, ensure_ascii=False, indent=2)

    with open(os.path.join("cfg/script/GenV2", version, "Cfg/CfgTypes.lua")) as f:
        types = f.read().replace("return {InitTypes = InitTypes}", "")
    with open(os.path.join("cfg/script/GenV2", version, "Cfg/CfgHelper.lua")) as f:
        lua = LuaRuntime(unpack_returned_tuples=True)
        helper = lua.execute(types + replace_enum_string(f.read()))
    with open("cfg/config_helper.json", "w", encoding="utf-8") as f:
        result = {}
        temp_outer = {}
        for k, v in helper.items():
            if k != "CommonHelper":
                for kk, vv in v.items():
                    reverse_map = {}
                    enum_map = {}
                    for j, value in vv.items():
                        reverse_map[value] = j
                    for j in sorted(reverse_map):
                        enum_map[reverse_map[j]] = j
                    temp_outer[f'{k}.{kk}'] = enum_map
            else:
                temp_outer[k] = {}
                for kk, vv in v.items():
                    temp_outer[k][kk] = vv
        for k in sorted(temp_outer):
            result[k] = temp_outer[k]

        json.dump(result, f, ensure_ascii=False, indent=2)
