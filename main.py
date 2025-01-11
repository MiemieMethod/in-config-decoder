from src.lua import decode_luas
from src.config import decode_configs

if __name__ == '__main__':
    I_N_DATA_PATH = r'E:/I-N-Data'  # change here to your path

    decode_luas(I_N_DATA_PATH)
    decode_configs(I_N_DATA_PATH)