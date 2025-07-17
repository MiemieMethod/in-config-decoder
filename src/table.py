
from perfect import *

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
                'Template1': buf.read_array(ByteBuf.read_int, False),
                'Template2': buf.read_array(ByteBuf.read_int, False), # comment this in cbt2
                'Template3': buf.read_array(ByteBuf.read_int, False), # comment this in cbt2
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
                'CollectionReward': buf.read_int(),
                'unk23': buf.read_int(),
                'unk24': buf.read_int(),
                'ObtainMethod': buf.read_array(ByteBuf.read_int, False)
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
                    'Major': buf.read_int(),
                    'unk6': buf.read_int(),
                    'Tag': buf.read_array(ByteBuf.read_int, False),
                    'unk8': buf.read_int(),
                    'unk9': buf.read_int(),
                    'unk10': buf.read_array(ByteBuf.read_int, False),
                    'unk11': buf.read_array(ByteBuf.read_int, False),
                    'unk12': buf.read_array(ByteBuf.read_int, False),
                    'unk13': buf.read_int(),
                    'unk14': buf.read_array(lambda buf: ByteBuf.read_bytes(buf).decode('utf-8'), False), # comment this in cbt2
                    'unk15': buf.read_array(lambda buf: ByteBuf.read_bytes(buf).decode('utf-8'), False),
                    'unk16': buf.read_array(ByteBuf.read_int, False),
                    'Comment1NPC': buf.read_array(ByteBuf.read_int, False),
                    'Comment1Key': buf.read_bytes().decode('utf-8'),
                    'Comment1Text': buf.read_bytes().decode('utf-8'),
                    'Comment2NPC': buf.read_array(ByteBuf.read_int, False),
                    'Comment2Key': buf.read_bytes().decode('utf-8'),
                    'Comment2Text': buf.read_bytes().decode('utf-8'),
                    'ID': buf.read_int(),
                    'unk17': buf.read_int(),
                    'ObtainMethod': buf.read_array(ByteBuf.read_int, False) # comment this in cbt2
                }
            elif type == -1078125975:
                content = {
                    'ItemType': type,
                    'ItemID': buf.read_int(),
                    'SkeletonMesh': buf.read_bytes().decode('utf-8'),
                    'BodyMesh': buf.read_array(lambda buf: ByteBuf.read_bytes(buf).decode('utf-8'), False),
                    'unk1': buf.read_array(ByteBuf.read_int, False),
                    'unk2': buf.read_array(ByteBuf.read_int, False),
                    'unk3': buf.read_array(ByteBuf.read_int, False),
                    'Niagara': buf.read_array(lambda buf: ByteBuf.read_bytes(buf).decode('utf-8'), False),
                    'Province': buf.read_int(),
                    'ShowpicTexture': buf.read_bytes().decode('utf-8'), # comment this in cbt2
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
                'CategoryID': buf.read_int(),
                'AttributeID': buf.read_int(),
                'DisplayTypeID': buf.read_int(),
                'unk3': buf.read_int(), # comment this line in 1.0
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
                'unk9': buf.read_int(), # comment below this line in cbt2
                'unk10': buf.read_int(),
                'unk11': buf.read_int(),
                'unk12': buf.read_int(),
                'unk13': buf.read_int(),
                'unk14': buf.read_int(),
                'unk15': buf.read_int(),
                'unk16': buf.read_int(),
                'GalleryScore': buf.read_int(),
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
                'unk3': buf.read_array(lambda buf: ByteBuf.read_bytes(buf).decode('utf-8'), False), # comment this in cbt2
                'unk4': buf.read_array(lambda buf: ByteBuf.read_bytes(buf).decode('utf-8'), False), # comment this in cbt2
                'unk5': buf.read_int(),
                'StartDialogue': buf.read_array(lambda buf: ByteBuf.read_bytes(buf).decode('utf-8'), False),
                'BubbleDialogue': buf.read_array(lambda buf: ByteBuf.read_bytes(buf).decode('utf-8'), False),
                'unk7': buf.read_array(ByteBuf.read_int, False),
                'HandHeldObject': buf.read_array(lambda buf: ByteBuf.read_bytes(buf).decode('utf-8'), False),
                'Warning': 'after this is a lot of complex data'
            }
            self.cache = content
        return self.cache


class ClothesAttributeFactorObject(SerializableObject):
    NAME = "ClothesAttributeFactor"
    ID = 5

    def __init__(self):
        self.cache = None

    def serialize(self, buf: ByteBuf):
        pass

    def deserialize(self, buf: ByteBuf):
        if self.cache is None:
            key = buf.read_int()
            content = {
                'ID': key,
                'Value': buf.read_float(),
            }
            self.cache = content
        return self.cache


class ClothesAttributeRankObject(SerializableObject):
    NAME = "ClothesAttributeRank"
    ID = 6

    def __init__(self):
        self.cache = None

    def serialize(self, buf: ByteBuf):
        pass

    def deserialize(self, buf: ByteBuf):
        if self.cache is None:
            key = buf.read_int()
            content = {
                'ID': key,
                'Text': buf.read_bytes().decode('utf-8'),
                'Min': buf.read_int(),
                'Max': buf.read_int(),
            }
            self.cache = content
        return self.cache


class ClothersTagInfoObject(SerializableObject):
    NAME = "ClothersTagInfo"
    ID = 7

    def __init__(self):
        self.cache = None

    def serialize(self, buf: ByteBuf):
        pass

    def deserialize(self, buf: ByteBuf):
        if self.cache is None:
            key = buf.read_int()
            content = {
                'TagID': key,
                'NameKey': buf.read_bytes().decode('utf-8'),
                'NameText': buf.read_bytes().decode('utf-8'),
                'Texture': buf.read_array(lambda buf: ByteBuf.read_bytes(buf).decode('utf-8'), False),
                'unk1': buf.read_array(ByteBuf.read_int, False),
            }
            self.cache = content
        return self.cache


class ClothesRenewNormalInfoObject(SerializableObject):
    NAME = "ClothesRenewNormalInfo"
    ID = 8

    def __init__(self):
        self.cache = None

    def serialize(self, buf: ByteBuf):
        pass

    def deserialize(self, buf: ByteBuf):
        if self.cache is None:
            key = buf.read_int()
            content = {
                'ClassID': key,
                'Rarity': buf.read_int(),
                'BaseIncrementStats': buf.read_int(),
                'NormalMaterial': buf.read_array(lambda buf: [ByteBuf.read_int(buf), ByteBuf.read_int(buf)], False),
                'SpecialMaterial': buf.read_array(lambda buf: [ByteBuf.read_int(buf), ByteBuf.read_int(buf)], False),
            }
            self.cache = content
        return self.cache


class ClothesLevelNormalInfoObject(SerializableObject):
    NAME = "ClothesLevelNormalInfo"
    ID = 9

    def __init__(self):
        self.cache = None

    def serialize(self, buf: ByteBuf):
        pass

    def deserialize(self, buf: ByteBuf):
        def subdeserializer(buf: ByteBuf):
            content = {
                'SubID': buf.read_int(),
                'CurrentLevel': buf.read_int(),
                'BaseIncrementStats': buf.read_int(),
                'subunk4': buf.read_array(ByteBuf.read_long, False),
                'ConditionKey': buf.read_bytes().decode('utf-8'),
                'ConditionText': buf.read_bytes().decode('utf-8'),
                'Material': buf.read_array(lambda buf: [ByteBuf.read_int(buf), ByteBuf.read_int(buf)], False),
            }
            return content

        if self.cache is None:
            key = buf.read_int()
            content = {
                'ClassID': key,
                'Rarity': buf.read_int(),
                'Condition': buf.read_array(subdeserializer, False),
            }
            self.cache = content
        return self.cache


class SuitFormulaObject(SerializableObject):
    NAME = "SuitFormula"
    ID = 10

    def __init__(self):
        self.cache = None

    def serialize(self, buf: ByteBuf):
        pass

    def deserialize(self, buf: ByteBuf):
        if self.cache is None:
            key = buf.read_int()
            content = {
                'FormulaItemID': key,
                'ItemID': buf.read_int(),
                'unk1': buf.read_int(),
                'unk2': buf.read_int(),
                'unk3': buf.read_int(),
                'Material': buf.read_array(lambda buf: [ByteBuf.read_int(buf), ByteBuf.read_int(buf)], False),
            }
            self.cache = content
        return self.cache


class GalleryObtainMethodObject(SerializableObject):
    NAME = "GalleryObtainMethod"
    ID = 11

    def __init__(self):
        self.cache = None

    def serialize(self, buf: ByteBuf):
        pass

    def deserialize(self, buf: ByteBuf):
        if self.cache is None:
            key = buf.read_int()
            content = {
                'MethodID': key,
                'DescriptionKey': buf.read_bytes().decode('utf-8'),
                'DescriptionName': buf.read_bytes().decode('utf-8'),
                'Texture': buf.read_bytes().decode('utf-8'),
            }
            self.cache = content
        return self.cache


class ItemV2Object(SerializableObject):
    NAME = "ItemV2"
    ID = 12

    def __init__(self):
        self.cache = None

    def serialize(self, buf: ByteBuf):
        pass

    def deserialize(self, buf: ByteBuf):
        if self.cache is None:
            key = buf.read_int()
            content = {
                'ItemID': key,
                'CategoryID': buf.read_int(),
                'unk1': buf.read_int(),
                'unk2': buf.read_int(),
                'Texture': buf.read_bytes().decode('utf-8'),
                'unk3': buf.read_int(),
            }
            self.cache = content
        return self.cache


class DisplayTypeInfoObject(SerializableObject):
    NAME = "DisplayTypeInfo"
    ID = 13

    def __init__(self):
        self.cache = None

    def serialize(self, buf: ByteBuf):
        pass

    def deserialize(self, buf: ByteBuf):
        if self.cache is None:
            key = buf.read_int()
            content = {
                'ID': key,
                '_ID': buf.read_int(),
                'TypeKey': buf.read_bytes().decode('utf-8'),
                'TypeName': buf.read_bytes().decode('utf-8'),
                'CommonTexture': buf.read_bytes().decode('utf-8'),
                'unk1': buf.read_int(),
                'RewardTexture': buf.read_bytes().decode('utf-8'),
                'SourceDescriptionKey': buf.read_bytes().decode('utf-8'),
                'SourceDescriptionText': buf.read_bytes().decode('utf-8'),
                'unk2': buf.read_long(),
            }
            self.cache = content
        return self.cache


class MagicBallInfoObject(SerializableObject):
    NAME = "MagicBallInfo"
    ID = 14

    def __init__(self):
        self.cache = None

    def serialize(self, buf: ByteBuf):
        pass

    def deserialize(self, buf: ByteBuf):
        if self.cache is None:
            key = buf.read_int()
            content = {
                'ID': key,
                'SuitKey': buf.read_bytes().decode('utf-8'),
                'SuitText': buf.read_bytes().decode('utf-8'),
                'SuitID': buf.read_int(),
                'Type': buf.read_int(),
                'unk2': buf.read_int(),
                'unk3': buf.read_int(),
                'unk4': buf.read_array(ByteBuf.read_long, False),
                'unk6': buf.read_int(),
                'unk7': buf.read_int(),
                'Tag': buf.read_int(),
                'Animation': buf.read_bytes().decode('utf-8'),
                'Stats': buf.read_array(ByteBuf.read_long, False),
                'unk10': buf.read_int(),
                'unk8': buf.read_int(),
                'unk9': buf.read_array(ByteBuf.read_long, False),

            }
            self.cache = content
        return self.cache


class MagicBallChangeInfoObject(SerializableObject):
    NAME = "MagicBallChangeInfo"
    ID = 15

    def __init__(self):
        self.cache = None

    def serialize(self, buf: ByteBuf):
        pass

    def deserialize(self, buf: ByteBuf):
        if self.cache is None:
            key = buf.read_int()
            content = {
                'ID': key,
                'unk1': buf.read_int(),
                'unk2': buf.read_int(),
                'unk3': buf.read_int(),
                'unk4': buf.read_int(),
                'unk5': buf.read_int(),

            }
            self.cache = content
        return self.cache


class BallLevelUpInfoObject(SerializableObject):
    NAME = "BallLevelUpInfo"
    ID = 16

    def __init__(self):
        self.cache = None

    def serialize(self, buf: ByteBuf):
        pass

    def deserialize(self, buf: ByteBuf):
        if self.cache is None:
            key = buf.read_int()
            content = {
                'Rarity': key,
                'CurrentLevel': buf.read_int(),
                'Exp': buf.read_int(),
                'unk3': buf.read_float(),
                'unk4': buf.read_int(),
                'BaseIncrementStats': buf.read_int(),

            }
            self.cache = content
        return self.cache
