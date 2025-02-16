import os
import struct
import subprocess

from concurrent.futures import ProcessPoolExecutor, as_completed

OPCODE_MAP = {
    0xa: 0,
    0: 1,
    1: 2,
    2: 3,
    3: 4,
    4: 5,
    5: 6,
    6: 7,
    7: 8,
    8: 9,
    9: 10,
}

OPCODE_INCREMENTS = [0xb, 0x10, 0x15, 0x17, 0x19, 0x1b, 0x37, 0x3c, 0x3e, 0x45, 0x4c, 0x4f, 0x52, 0x56, 0x59, 0x5d, 0x5f, 0x61, 0x63, 0x65]

def replace_opcode(modified_opcode):
    original_opcode = OPCODE_MAP[modified_opcode] if modified_opcode in OPCODE_MAP else modified_opcode
    inst_value_offset = 0
    for increment in OPCODE_INCREMENTS:
        if original_opcode > increment:
            inst_value_offset -= 1
    original_opcode += inst_value_offset
    return original_opcode

def read_size(file):
    array = []
    while True:
        byte = file.read(1)
        if not byte:
            raise EOFError("Unexpected end of file")
        byte_value = byte[0]
        array.append(byte_value)
        if (byte_value & 0x80) != 0 or len(array) >= 9:
            break
    return transform_size_array(array)

def transform_size_array(array):
    res = 0
    for i in range(len(array) - 1):
        res <<= 7
        res |= array[i] & 0x7F
    res <<= 7
    res |= array[-1] & 0x7F
    return res

def read_lua_string(file):
    size = read_size(file)
    if size == 0:
        return None
    return file.read(size - 1).decode('utf-8')

def read_constant(file):
    type_byte = struct.unpack('<B', file.read(1))[0]
    if type_byte == 3:
        return struct.unpack('<Q', file.read(8))[0]
    elif type_byte == 0x13:
        return struct.unpack('<d', file.read(8))[0]
    elif type_byte in (0x4, 0x14):
        return read_lua_string(file)
    return None

def read_code(file, code_pos):
    code_pos.append(file.tell())
    return struct.unpack('<BBBB', file.read(4))

def read_vector(file, read_element):
    size = read_size(file)
    return [read_element(file) for _ in range(size)]

def read_abs_line_info(file):
    pc = read_size(file)
    line = read_size(file)
    return {'pc': pc, 'line': line}

def read_local_var(file):
    varname = read_lua_string(file)
    startpc = read_size(file)
    endpc = read_size(file)
    return {'varname': varname, 'startpc': startpc, 'endpc': endpc}

def read_debug_info(file):
    line_info = read_vector(file, lambda f: struct.unpack('<b', f.read(1))[0])
    abs_line_info = read_vector(file, read_abs_line_info)
    local_vars = read_vector(file, read_local_var)
    upvalues = read_vector(file, read_lua_string)
    return {
        'line_info': line_info,
        'abs_line_info': abs_line_info,
        'local_vars': local_vars,
        'upvalues': upvalues
    }

def read_lua_function(file):
    source = read_lua_string(file)
    # line_defined = read_size(file)
    # last_line_defined = read_size(file)
    # number_of_parameters = struct.unpack('<B', file.read(1))[0]
    # is_vararg = struct.unpack('<B', file.read(1))[0]
    # maxstacksize = struct.unpack('<B', file.read(1))[0]
    #
    # code_pos = []
    # code = read_vector(file, lambda f: read_code(f, code_pos))
    # constants = read_vector(file, read_constant)
    # upvalues = read_vector(file, lambda f: struct.unpack('<BBB', f.read(3)))
    # protos = read_vector(file, read_lua_function)
    # debug_info = read_debug_info(file)

    return {
        'source': source,
        # 'line_defined': line_defined,
        # 'last_line_defined': last_line_defined,
        # 'number_of_parameters': number_of_parameters,
        # 'is_vararg': is_vararg,
        # 'maxstacksize': maxstacksize,
        # 'code_pos': code_pos,
        # 'code': code,
        # 'constants': constants,
        # 'upvalues': upvalues,
        # 'protos': protos,
        # 'debug_info': debug_info
    }


def read_lua_file(file):
    header_format = '<IBB6sBBBQd'
    header_size = struct.calcsize(header_format)
    header_data = file.read(header_size)
    header = struct.unpack(header_format, header_data)

    size_of_upvalues = struct.unpack('<B', file.read(1))[0]
    func = read_lua_function(file)

    return {
        'header': header,
        'size_of_upvalues': size_of_upvalues,
        'function': func
    }


def parse_lua_bytecode(filename):
    with open(filename, 'rb') as file:
        return read_lua_file(file)

def fix_function(data, func):
    for i, code_pos in enumerate(func['code_pos']):
        masked_code = func['code'][i][0] & 0x80
        data[code_pos] = masked_code + replace_opcode(func['code'][i][0] & 0x7F)
    for proto in func['protos']:
        fix_function(data, proto)
    return func

def fix_lua_bytecode(filename):
    lua_bytecode = parse_lua_bytecode(filename)

    with open(filename, 'rb') as file:
        data = bytearray(file.read())
    # data[4] = 84
    # fix_function(data, lua_bytecode['function'])
    output_path = lua_bytecode['function']['source'].split('X6Game/Content/Script/')[-1]
    return output_path, data

def decode_lua_bytecode(output_base, full_file_path):
    if os.path.getsize(full_file_path) == 0:
        return None
    print(f'Decoding {os.path.basename(full_file_path)}')
    output_path, data = fix_lua_bytecode(full_file_path)
    output_path = os.path.join(output_base, output_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path + 'c', 'wb') as f:
        f.write(data)
    subprocess.run(['java', '-jar', 'unluac.jar', output_path + 'c', '>', output_path], shell=True)


def decode_luas(I_N_DATA_PATH):
    output_base = r'cfg/script'
    script_path = os.path.join(I_N_DATA_PATH, r'X6Game/Content/Script')

    lua_files = [
        os.path.join(root, file)
        for root, _, files in os.walk(script_path)
        for file in files if file.endswith('.lua')
    ]

    completed = 0

    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(decode_lua_bytecode, output_base, file) for file in lua_files]
        for future in as_completed(futures):
            future.result()

            completed += 1

            print(f"{completed} / {len(lua_files)}")
