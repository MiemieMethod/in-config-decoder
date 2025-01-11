import json
import os

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

def decode_configs(I_N_DATA_PATH):
    with open("cfg/script/GenV2/Cfg/CfgTypes.lua") as f:
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
    end').replace('list = UENewTable', 'list = UENewList'))

    init_function = config.InitTypes

    init_data = init_function(methods)

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

                    orders = {}
                    name = luaTable._name
                    # print(name)
                    this_bean = None
                    for j in init_data.beans:
                        if init_data.beans[j]._name == name:
                            this_bean = init_data.beans[j]
                            break
                    if this_bean is None:
                        table = None
                        if hasattr(luaTable, '_type'):
                            if luaTable._type == 'list':
                                table = []
                            elif luaTable._type == 'dict':
                                table = {}
                            for j in luaTable:
                                if j == '_type':
                                    continue
                                if isinstance(table, list):
                                    table.append(luaTable[j])
                                    parseLuatable(table, j - 1, luaTable[j])
                                elif isinstance(table, dict):
                                    parseLuatable(table, j, luaTable[j])
                            return table
                        else:
                            print(f'Bean {name} not found')
                    for field in this_bean._name2number:
                        orders[this_bean._name2number[field]] = field
                    built = {
                        '_name': name,
                        '_id': luaTable._id
                    }
                    luatable_type = type(luaTable)
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
        loaded_table = config_table.load(os.path.join(I_N_DATA_PATH, r'X6Game/Content/config_output'))
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

        os.makedirs(f'cfg/config_output/{table.value_type.split('.')[0]}', exist_ok=True)
        with open(f'cfg/config_output/{table.file.replace('.bin', '.json').replace('.', '/', 1)}', 'w', encoding='utf-8') as f:
            json.dump(loaded_table, f, ensure_ascii=False, indent=2)