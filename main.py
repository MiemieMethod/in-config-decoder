import os

from src.i18n import decode_locres
from src.lua import decode_luas, decode_lua_bytecode
from src.config import decode_configs, decode_helper

def decode_lua_and_configs(I_N_DATA_PATH):
    decode_luas(I_N_DATA_PATH)
    decode_configs(I_N_DATA_PATH)
    decode_helper(I_N_DATA_PATH)

def decode_infinity_nikki_data_repo(I_N_DATA_PATH):
    decode_lua_bytecode(r'cfg/script', os.path.join(I_N_DATA_PATH, r'X6Game/Content/Script/GenV2/Cfg/1634995571.lua'))
    decode_configs(I_N_DATA_PATH, True)
    decode_locres(I_N_DATA_PATH)

def decode_just_configs(I_N_DATA_PATH):
    decode_lua_bytecode(r'cfg/script', os.path.join(I_N_DATA_PATH, r'X6Game/Content/Script/GenV2/Cfg/1634995571.lua'))
    decode_configs(I_N_DATA_PATH)

if __name__ == '__main__':
    I_N_DATA_PATH = r'E:/I-N-Data'  # change here to your path
    decode_infinity_nikki_data_repo(I_N_DATA_PATH)

