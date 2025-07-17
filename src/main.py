import json
import os
import subprocess

from table import *
from post_process import post
from diff import diff

I_N_DATA_PATH = r'E:\I-N-Data' # change here to your path

LOCALES = [
    'zh',
    'zh-Hant',
    # 'zh-SG', // Singapore Chinese is actually the same as Simplified Chinese
    'en',
    'ja-JP',
    'ko',
    'th',
    'id',
    'pt',
    'es',
    'fr',
    'de',
    'it',
]


def loadTable(name: str, file_name: str, value_type: str, mode: str, registry: TypeRegistry):
    config_table = ConfigTable(
        name=name,
        file_name=file_name,
        value_type=value_type,
        mode=mode,
        registry=registry
    )
    table = config_table.load(os.path.join(I_N_DATA_PATH, r'X6Game/Content/config_output'))
    # print(table)
    result = {}
    if mode == 'map':
        for key, value in table.items():
            result[key] = value.deserialize(ByteBuf(b''))
    elif mode == 'bmap':
        for key, value in table.items():
            for k, v in value.items():
                if key not in result:
                    result[key] = {}
                result[key][k] = v.deserialize(ByteBuf(b''))
    os.makedirs('cfg', exist_ok=True)
    with open(f'cfg/{name}.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

# def decodeLocres():
#     os.makedirs('cfg', exist_ok=True)
#     subprocess.run(['./UnrealLocres', 'export', os.path.join(I_N_DATA_PATH, r'X6Game/Content/Localization/Game/zh/Game.locres'), '-f', 'csv', '-o', 'cfg/Game.csv'], encoding='utf-8')


def decodeLocres():
    os.makedirs('ol', exist_ok=True)
    for locale in LOCALES:
        subprocess.run(['./UnrealLocres', 'export', os.path.join(I_N_DATA_PATH, f'X6Game/Content/Localization/Game/{locale}/Game.locres'), '-f', 'csv', '-o', f'cfg/Game_{locale}.csv'], encoding='utf-8')


if __name__ == '__main__':
    decodeLocres()

    registry = TypeRegistry()
    registry.register_class(SuitObject)
    loadTable('clothes.TbSuit', 'clothes.TbSuit.bin', 'Suit', 'map', registry)
    registry.register_class(ItemExtraObject)
    loadTable('item.TbItemExtra', 'item.TbItemExtra.bin', 'ItemExtra', 'map', registry)
    registry.register_class(ItemObject)
    loadTable('item.TbItem', 'item.TbItem.bin', 'Item', 'map', registry)
    registry.register_class(ItemV2Object)
    loadTable('item.TbItemV2', 'item.TbItemV2.bin', 'ItemV2', 'bmap', registry)
    registry.register_class(CharacterInfoObject)
    loadTable('character.TbCharacterInfo', 'character.TbCharacterInfo.bin', 'CharacterInfo', 'map', registry)
    registry.register_class(ClothesAttributeFactorObject)
    loadTable('clothes.TbClothesAttributeFactor', 'clothes.TbClothesAttributeFactor.bin', 'ClothesAttributeFactor', 'map', registry)
    registry.register_class(ClothesAttributeRankObject)
    loadTable('clothes.TbClothesAttributeRank', 'clothes.TbClothesAttributeRank.bin', 'ClothesAttributeRank', 'map', registry)
    registry.register_class(ClothersTagInfoObject)
    loadTable('clothes.TbClothersTagInfo', 'clothes.TbClothersTagInfo.bin', 'ClothersTagInfo', 'map', registry)
    registry.register_class(ClothesRenewNormalInfoObject)
    loadTable('clothes.TbClothesRenewNormalInfo', 'clothes.TbClothesRenewNormalInfo.bin', 'ClothesRenewNormalInfo', 'bmap', registry)
    registry.register_class(ClothesLevelNormalInfoObject)
    loadTable('clothes.TbClothesLevelNormalInfo', 'clothes.TbClothesLevelNormalInfo.bin', 'ClothesLevelNormalInfo', 'bmap', registry)
    registry.register_class(SuitFormulaObject)
    loadTable('clothes.TbSuitFormula', 'clothes.TbSuitFormula.bin', 'SuitFormula', 'map', registry)
    registry.register_class(GalleryObtainMethodObject)
    loadTable('gallery.TbGalleryObtainMethod', 'gallery.TbGalleryObtainMethod.bin', 'GalleryObtainMethod', 'map', registry)
    registry.register_class(DisplayTypeInfoObject)
    loadTable('item.TbDisplayTypeInfo', 'item.TbDisplayTypeInfo.bin', 'DisplayTypeInfo', 'map', registry)
    registry.register_class(MagicBallInfoObject)
    loadTable('magic_ball.TbMagicBallInfo', 'magic_ball.TbMagicBallInfo.bin', 'MagicBallInfo', 'map', registry)
    # registry.register_class(MagicBallChangeInfoObject)
    # loadTable('magic_ball.TbMagicBallChangeInfo', 'magic_ball.TbMagicBallChangeInfo.bin', 'MagicBallChangeInfo', 'map', registry)
    registry.register_class(BallLevelUpInfoObject)
    loadTable('magic_ball.TbBallLevelUpInfo', 'magic_ball.TbBallLevelUpInfo.bin', 'BallLevelUpInfo', 'bmap', registry)


    post()

    diff()