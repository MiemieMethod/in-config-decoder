import json
import os
import subprocess

from perfect import *

I_N_DATA_PATH = r'E:/I-N-Data' # change here to your path

class SuitObject(SerializableObject):
    NAME = "Suit"
    ID = 1

    def __init__(self):
        self.cache = None

    def serialize(self, buf: ByteBuf):
        pass

    def deserialize(self, buf: ByteBuf):
        if self.cache is None:
            key = buf.read_int()
            content = {
                'SuitID': key,
                'NameText': buf.read_bytes().decode('utf-8'),
                'NameKey': buf.read_bytes().decode('utf-8'),
                'unk1': buf.read_int(),
                'Rarity': buf.read_int(),
                'unk3': buf.read_int(),
                'unk4': buf.read_int(),
                'Texture1': buf.read_bytes().decode('utf-8'),
                'Texture2': buf.read_bytes().decode('utf-8'),
                'Texture3': buf.read_bytes().decode('utf-8'),
                'Parts': buf.read_array(ByteBuf.read_int, False),
                'unk6': buf.read_int(),
                'unk7': buf.read_array(ByteBuf.read_int, False),
                'unk8': buf.read_array(ByteBuf.read_int, False),
                'unk9': buf.read_int(),
                'unk10': buf.read_int(),
                'unk11': buf.read_int(),
                'unk12': buf.read_int(),
                'unk13': buf.read_array(ByteBuf.read_int, False),
                'unk14': buf.read_array(ByteBuf.read_int, False),
                'unk15': buf.read_array(ByteBuf.read_int, False),
                'DescriptionText': buf.read_bytes().decode('utf-8'),
                'DescriptionKey': buf.read_bytes().decode('utf-8'),
                'unk16': buf.read_int(),
                'unk17': buf.read_int(),
                'Template1': buf.read_bytes().decode('utf-8'),
                'Template2': buf.read_bytes().decode('utf-8'),
                'Template3': buf.read_bytes().decode('utf-8'),
                'Comment1NPC': buf.read_array(ByteBuf.read_int, False),
                'Comment1Key': buf.read_bytes().decode('utf-8'),
                'Comment1Text': buf.read_bytes().decode('utf-8'),
                'Comment2NPC': buf.read_array(ByteBuf.read_int, False),
                'Comment2Key': buf.read_bytes().decode('utf-8'),
                'Comment2Text': buf.read_bytes().decode('utf-8'),
                'unk18': buf.read_int(),
                'unk19': buf.read_array(ByteBuf.read_int, False),
                'unk20': buf.read_array(ByteBuf.read_int, False),
                'unk21': buf.read_array(ByteBuf.read_int, False),
                'unk22': buf.read_int(),
                'unk23': buf.read_int(),
                'unk24': buf.read_int(),
                'unk25': buf.read_array(ByteBuf.read_int, False)
            }
            self.cache = content
        return self.cache

class ItemExtraObject(SerializableObject):
    NAME = "ItemExtra"
    ID = 2

    def __init__(self):
        self.cache = None

    def serialize(self, buf: ByteBuf):
        pass

    def deserialize(self, buf: ByteBuf):
        if self.cache is None:
            type = buf.read_int()
            if type == 1659907149:
                content = {
                    'ItemType': type,
                    'ItemID': buf.read_int(),
                    'SkeletonMesh': buf.read_bytes().decode('utf-8'),
                    'unk1': buf.read_array(lambda buf: ByteBuf.read_bytes(buf).decode('utf-8'), False),
                    'unk2': buf.read_array(lambda buf: ByteBuf.read_bytes(buf).decode('utf-8'), False),
                    'unk3': buf.read_bytes().decode('utf-8'),
                    'ShowpicTexture': buf.read_bytes().decode('utf-8'),
                    'Rarity': buf.read_int(),
                    'Stats': buf.read_array(ByteBuf.read_int, False),
                    'unk5': buf.read_int(),
                    'unk6': buf.read_int(),
                    'unk7': buf.read_array(ByteBuf.read_int, False),
                    'unk8': buf.read_int(),
                    'unk9': buf.read_int(),
                    'unk10': buf.read_array(ByteBuf.read_int, False),
                    'unk11': buf.read_array(ByteBuf.read_int, False),
                    'unk12': buf.read_array(ByteBuf.read_int, False),
                    'unk13': buf.read_int(),
                    'unk14': buf.read_array(lambda buf: ByteBuf.read_bytes(buf).decode('utf-8'), False),
                    'unk15': buf.read_array(lambda buf: ByteBuf.read_bytes(buf).decode('utf-8'), False),
                    'unk16': buf.read_array(ByteBuf.read_int, False),
                    'Comment1NPC': buf.read_array(ByteBuf.read_int, False),
                    'Comment1Key': buf.read_bytes().decode('utf-8'),
                    'Comment1Text': buf.read_bytes().decode('utf-8'),
                    'Comment2NPC': buf.read_array(ByteBuf.read_int, False),
                    'Comment2Key': buf.read_bytes().decode('utf-8'),
                    'Comment2Text': buf.read_bytes().decode('utf-8'),
                    'ID': buf.read_int(),
                    'unk17': buf.read_array(lambda buf: ByteBuf.read_bytes(buf).decode('utf-8'), False),
                }
            elif type == -1078125975:
                content = {
                    'ItemType': type,
                    'ItemID': buf.read_int(),
                    'SkeletonMesh': buf.read_bytes().decode('utf-8'),
                    'unk1': buf.read_int(),
                    'unk2': buf.read_int(),
                    'unk3': buf.read_int(),
                    'Niagara': buf.read_array(lambda buf: ByteBuf.read_bytes(buf).decode('utf-8'), False),
                    'ShowpicTexture': buf.read_array(lambda buf: ByteBuf.read_bytes(buf).decode('utf-8'), False),
                }
            elif type == 0:
                content = {
                    'ItemType': type,
                }
            elif type == 1034622210:
                content = {
                    'ItemType': type,
                    'ItemID': buf.read_int(),
                    'unk1': buf.read_int(),
                    'LetterBeginKey': buf.read_bytes().decode('utf-8'),
                    'LetterBeginText': buf.read_bytes().decode('utf-8'),
                    'LetterKey': buf.read_bytes().decode('utf-8'),
                    'LetterText': buf.read_bytes().decode('utf-8'),
                    'LetterEndKey': buf.read_bytes().decode('utf-8'),
                    'LetterEndText': buf.read_bytes().decode('utf-8'),
                }
            else:
                content = {
                    'ItemType': type,
                    'ItemID': buf.read_int(),
                    'Warrning': 'Sorry, for this type of item I did not implement the deserialization method yet.'
                }
            self.cache = content
        return self.cache

class ItemObject(SerializableObject):
    NAME = "Item"
    ID = 3

    def __init__(self):
        self.cache = None

    def serialize(self, buf: ByteBuf):
        pass

    def deserialize(self, buf: ByteBuf):
        if self.cache is None:
            key = buf.read_int()
            content = {
                'ItemID': key,
                'NameText': buf.read_bytes().decode('utf-8'),
                'NameKey': buf.read_bytes().decode('utf-8'),
                'unk1': buf.read_int(),
                'unk2': buf.read_int(),
                'unk3': buf.read_int(),
                'unk4': buf.read_int(),
                'Rarity': buf.read_int(),
                'Texture1': buf.read_bytes().decode('utf-8'),
                'Texture2': buf.read_bytes().decode('utf-8'),
                'unk5': buf.read_int(),
                'unk6': buf.read_int(),
                'unk7': buf.read_int(),
                'unk8': buf.read_int(),
                'UseText': buf.read_bytes().decode('utf-8'),
                'UseKey': buf.read_bytes().decode('utf-8'),
                'DescriptionText': buf.read_bytes().decode('utf-8'),
                'DescriptionKey': buf.read_bytes().decode('utf-8'),
                'unk9': buf.read_int(),
                'unk10': buf.read_int(),
                'unk11': buf.read_int(),
                'unk12': buf.read_int(),
                'unk13': buf.read_int(),
                'unk14': buf.read_int(),
                'unk15': buf.read_int(),
                'unk16': buf.read_int(),
                'unk17': buf.read_int(),
                'unk18': buf.read_int(),
                'unk19': buf.read_array(ByteBuf.read_int, False),
                'unk20': buf.read_int(),
                'unk21': buf.read_int(),
                'unk22': buf.read_int(),
                'unk23': buf.read_int(),
            }
            self.cache = content
        return self.cache

class CharacterInfoObject(SerializableObject):
    NAME = "CharacterInfo"
    ID = 4

    def __init__(self):
        self.cache = None

    def serialize(self, buf: ByteBuf):
        pass

    def deserialize(self, buf: ByteBuf):
        if self.cache is None:
            key = buf.read_int()
            content = {
                'CharacterID': key,
                'Name': buf.read_array(lambda buf: ByteBuf.read_bytes(buf).decode('utf-8'), False),
                'unk1': buf.read_array(lambda buf: ByteBuf.read_bytes(buf).decode('utf-8'), False),
                'unk2': buf.read_bytes().decode('utf-8'),
                'unk3': buf.read_array(lambda buf: ByteBuf.read_bytes(buf).decode('utf-8'), False),
                'unk4': buf.read_array(lambda buf: ByteBuf.read_bytes(buf).decode('utf-8'), False),
                'unk5': buf.read_int(),
                'StartDialogue': buf.read_array(lambda buf: ByteBuf.read_bytes(buf).decode('utf-8'), False),
                'BubbleDialogue': buf.read_array(lambda buf: ByteBuf.read_bytes(buf).decode('utf-8'), False),
                'unk7': buf.read_array(ByteBuf.read_int, False),
                'HandHeldObject': buf.read_array(lambda buf: ByteBuf.read_bytes(buf).decode('utf-8'), False),
                'Warning': 'after this is a lot of complex data'
            }
            self.cache = content
        return self.cache


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
    for key, value in table.items():
        result[key] = value.deserialize(ByteBuf(b''))
    os.makedirs('cfg', exist_ok=True)
    with open(f'cfg/{name}.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

def decodeLocres():
    os.makedirs('cfg', exist_ok=True)
    subprocess.run(['./UnrealLocres', 'export', os.path.join(I_N_DATA_PATH, r'X6Game/Content/Localization/Game/en/Game.locres'), '-f', 'csv', '-o', 'cfg/Game.csv'], encoding='utf-8')

if __name__ == '__main__':
    decodeLocres()

    registry = TypeRegistry()
    registry.register_class(SuitObject)
    loadTable('clothes.TbSuit', 'clothes.TbSuit.bin', 'Suit', 'map', registry)
    registry.register_class(ItemExtraObject)
    loadTable('item.TbItemExtra', 'item.TbItemExtra.bin', 'ItemExtra', 'map', registry)
    registry.register_class(ItemObject)
    loadTable('item.TbItem', 'item.TbItem.bin', 'Item', 'map', registry)
    registry.register_class(CharacterInfoObject)
    loadTable('character.TbCharacterInfo', 'character.TbCharacterInfo.bin', 'CharacterInfo', 'map', registry)

    import csv
    texts = {}
    with open('cfg/Game.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            texts[row['key'][1:]] = row['source']

    with open('cfg/item.TbItemExtra.json', 'r', encoding='utf-8') as f:
        item_extra = json.load(f)

    with open('cfg/item.TbItem.json', 'r', encoding='utf-8') as f:
        item = json.load(f)

    with open('cfg/character.TbCharacterInfo.json', 'r', encoding='utf-8') as f:
        character_info = json.load(f)

    with open('cfg/clothes.TbSuit.json', 'r', encoding='utf-8') as f:
        suit = json.load(f)

    def getCharacterName(id):
        if str(id) not in character_info:
            return f'Character_{id}'
        char = character_info[str(id)]
        name = char['Name'][0] \
          .replace("NSLOCTEXT", '') \
          .replace("(", '') \
          .replace(")", '') \
          .replace("\"", '') \
          .split(', ') \
          [1]
        name = texts.get(name, f'Character_{id}')
        return name

    def joinCharacter(arr):
        return ' & '.join([getCharacterName(i) for i in arr])

    def generatePieces():
        result = ""
        for item_id in item_extra:
            _item = item_extra[item_id]
            if _item['ItemType'] == 1659907149:
                actual_item = item[item_id]
                result += texts.get(actual_item['NameKey'], actual_item['NameKey']) + '\n'
                result += texts.get(actual_item['UseKey'], actual_item['UseKey']) + '\n'
                result += texts.get(actual_item['DescriptionKey'], actual_item['DescriptionKey']) + '\n'
                result += 'Rarity: ' + str(actual_item['Rarity']) + '\n'
                result += 'BaseStats: ' + ', '.join([str(i) for i in _item['Stats']]) + '\n'
                result += 'Comments: \n'
                result += joinCharacter(_item['Comment1NPC']) + ': ' + texts.get(_item['Comment1Key'], _item['Comment1Key']) + '\n'
                result += joinCharacter(_item['Comment2NPC']) + ': ' + texts.get(_item['Comment2Key'], _item['Comment2Key']) + '\n'
                result += '\n'
        return result

    def generateSuits():
        result = ""
        for suit_id in suit:
            _suit = suit[suit_id]
            result += texts.get(_suit['NameKey'], _suit['NameKey']) + '\n'
            result += texts.get(_suit['DescriptionKey'], _suit['DescriptionKey']) + '\n'
            result += 'Rarity: ' + str(_suit['Rarity']) + '\n'
            result += 'Comments: \n'
            result += joinCharacter(_suit['Comment1NPC']) + ': ' + texts.get(_suit['Comment1Key'], _suit['Comment1Key']) + '\n'
            result += joinCharacter(_suit['Comment2NPC']) + ': ' + texts.get(_suit['Comment2Key'], _suit['Comment2Key']) + '\n'
            result += 'Pieces: \n'
            for piece in _suit['Parts']:
                if str(piece) not in item:
                    result += f'Item_{piece}\n'
                    continue
                actual_item = item[str(piece)]
                result += texts.get(actual_item['NameKey'], actual_item['NameKey']) + '\n'
            result += '\n'
        return result

    with open('cfg/pieces.txt', 'w', encoding='utf-8') as f:
        f.write(generatePieces())

    with open('cfg/suits.txt', 'w', encoding='utf-8') as f:
        f.write(generateSuits())