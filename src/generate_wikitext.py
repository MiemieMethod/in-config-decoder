import math
import shutil
import os
import json
import csv

en_texts = {}
with open(f'cfg/Game_en.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        en_texts[row['key']] = row['source']

with open(r'cfg/config_output/item/TbItem.json', 'r', encoding='utf-8') as f:
    item_table = json.load(f)

with open(r'cfg/config_output/item/TbItemExtra.json', 'r', encoding='utf-8') as f:
    item_extra_table = json.load(f)

with open(r'cfg/config_output/clothes/TbSuit.json', 'r', encoding='utf-8') as f:
    suit_table = json.load(f)

with open(r'cfg/config_output/clothes/TbSuitFormula.json', 'r', encoding='utf-8') as f:
    suit_formula_table = json.load(f)

with open(r'cfg/config_output/clothes/TbClothesAttributeFactor.json', 'r', encoding='utf-8') as f:
    clothes_attribute_factor_table = json.load(f)

with open(r'cfg/config_output/clothes/TbClothesAttributeRank.json', 'r', encoding='utf-8') as f:
    clothes_attribute_rank_table = json.load(f)

with open(r'cfg/config_output/character/TbCharacterInfo.json', 'r', encoding='utf-8') as f:
    character_table = json.load(f)

with open(r'cfg/config_output/evolution/TbSuitEvolution.json', 'r', encoding='utf-8') as f:
    suit_evolution_table = json.load(f)

with open(r'cfg/config_output/clothes/TbClothesMinorTypeInfo.json', 'r', encoding='utf-8') as f:
    clothes_minor_type_table = json.load(f)

with open(r'cfg/config_output/clothes/TbClothesClassify.json', 'r', encoding='utf-8') as f:
    clothes_classify_table = json.load(f)

with open(r'cfg/config_output/clothes/TbClothersPropInfo.json', 'r', encoding='utf-8') as f:
    clothes_prop_table = json.load(f)

with open(r'cfg/config_output/clothes/TbClothersTagInfo.json', 'r', encoding='utf-8') as f:
    clothes_tag_table = json.load(f)

with open(r'cfg/config_output/gallery/TbClothesGalleryBigTheme.json', 'r', encoding='utf-8') as f:
    gallery_theme_table = json.load(f)

with open(r'cfg/config_output/gallery/TbGalleryObtainMethod.json', 'r', encoding='utf-8') as f:
    gallery_obtain_method_table = json.load(f)

with open(r'cfg/config_output/gallery/TbClothesGallerySmallTheme.json', 'r', encoding='utf-8') as f:
    gallery_small_theme_table = json.load(f)



def generateGeneralMediaWikiTemplate(name, args: dict, save_at: str = ''):
    template = f'{{{{{name}\n'
    for key, value in args.items():
        if key.isdigit():
            template += f'|{value}\n'
        else:
            template += f'|{key}={value}\n'
    template += '}}'
    if len(args) <= 1:
        template = template.replace('\n', '')
    # print(template)
    if save_at:
        with open(save_at, 'w', encoding='utf-8') as f:
            f.write(template)
    return template

# generatePieceToSuitMapping
piece_to_suit_mapping = {}
for suit_id, suit in suit_table.items():
    for piece_id in suit['components']:
        piece_to_suit_mapping[piece_id] = suit_id

def getSuitIdFromPieceId(piece_id):
    return piece_to_suit_mapping[piece_id]

def getPieceDisplayType(piece_id):
    return item_table[str(piece_id)]['display_type']

def getPieceName(piece_id):
    return item_table[str(piece_id)]['name']

def getSuitName(suit_id):
    return suit_table[str(suit_id)]['suit_name']

def getEnText(key):
    return en_texts.get('/' + key, '')

def getPieceEnName(piece_id):
    piece = item_table[str(piece_id)]
    return getEnText(piece['l10nname'])

# generatePieceToFullEvolutionMapping, generateSuitToFullEvolutionMapping
piece_to_full_evolution_mapping = {}
suit_to_full_evolution_mapping = {}
for suit_id, suit_evolution_data in suit_evolution_table.items():
    suit_evolution_entry = [int(suit_id)]
    for evolution in suit_evolution_data['evolution_info']:
        suit_evolution_entry.insert(evolution['level'], evolution['suit_id'])
    for _suit_id in suit_evolution_entry:
        suit_to_full_evolution_mapping[_suit_id] = suit_evolution_entry

    for piece_id in suit_table[str(suit_id)]['components']:
        piece_evolution_entry = [piece_id]
        for evolution in suit_evolution_data['evolution_info']:
            new_suit_id = evolution['suit_id']
            new_suit_pieces = suit_table[str(new_suit_id)]['components']
            for new_piece_id in new_suit_pieces:
                if getPieceDisplayType(new_piece_id) == getPieceDisplayType(piece_id):
                    piece_evolution_entry.insert(evolution['level'], new_piece_id)
                    break
        for _piece_id in piece_evolution_entry:
            piece_to_full_evolution_mapping[_piece_id] = piece_evolution_entry

def getPieceFullEvolutionMapping(id):
    if id not in piece_to_full_evolution_mapping:
        return [id]
    return piece_to_full_evolution_mapping[id]

def getSuitFullEvolutionMapping(id):
    if id not in suit_to_full_evolution_mapping:
        return [id]
    return suit_to_full_evolution_mapping[id]

def generateEvolutionTabs(id):
    template_args = {}
    for i, piece_id in enumerate(getPieceFullEvolutionMapping(id)):
        template_args[f'tab{str(i + 1)}'] = getPieceName(piece_id)
    return generateGeneralMediaWikiTemplate('Evolution Tabs', template_args)

# generatePieceToGalleryMapping, generateSuitToGalleryMapping
piece_to_gallery_mapping = {}
suit_to_gallery_mapping = {}
for small_theme_id, small_theme in gallery_small_theme_table.items():
    for suit_part_id in small_theme['suit_parts_ids']:
        if str(suit_part_id) in suit_table:
            for suit_id in getSuitFullEvolutionMapping(suit_part_id):
                suit_to_gallery_mapping[suit_id] = small_theme_id
                for piece_id in suit_table[str(suit_id)]['components']:
                    piece_to_gallery_mapping[piece_id] = small_theme_id
        else:
            piece_to_gallery_mapping[suit_part_id] = small_theme_id

def getGallerySmallThemeName(id):
    return gallery_small_theme_table[str(id)]['name']

def getClothesMinorTypeName(id):
    return clothes_minor_type_table[str(id)]['show_name']

def getClothesPropName(id):
    return clothes_prop_table[str(id)]['show_name']

def getClothesTagName(id):
    return clothes_tag_table[str(id)]['show_name']

def getObtainMethodDesc(id):
    if str(id) not in gallery_obtain_method_table:
        return ''
    return gallery_obtain_method_table[str(id)]['desc']

# generateClothingToSketchMapping
clothing_to_sketch_mapping = {}
for sketch_id, sketch in suit_formula_table.items():
    clothing_to_sketch_mapping[sketch['ref_id']] = sketch['design_id']

def getSketchIdFromPieceId(piece_id):
    return clothing_to_sketch_mapping.get(piece_id, None)

def generateClothingInfobox(id):
    template_args = {
        'id': id,
    }
    if getPieceEnName(id) != '':
        template_args['preview'] = getPieceEnName(id) + ' Showpic.png'
        template_args['icon'] = getPieceEnName(id) + ' Icon.png'
    item = item_table[str(id)]
    extra = item_extra_table.get(str(id), {})
    template_args['title'] = getPieceName(id)
    template_args['set'] = getSuitName(getSuitIdFromPieceId(id)) if id in piece_to_suit_mapping else ''
    template_args['compendium'] = getGallerySmallThemeName(piece_to_gallery_mapping[id]) if id in piece_to_gallery_mapping else ''
    template_args['rarity'] = extra['clothers_quality']
    template_args['category'] = getClothesMinorTypeName(item['minor_type'])
    template_args['style'] = getClothesPropName(extra['major_prop'])
    for i, tag in enumerate(extra['clothers_tags']):
        template_args[f'attribute{i + 1}'] = getClothesTagName(tag)
    template_args['how_to_obtain'] = getObtainMethodDesc(extra['obtain_desc']).replace('。', '')
    template_args['description'] = item['desc']
    if getSketchIdFromPieceId(id):
        template_args['sketch_description'] = item_table[str(getSketchIdFromPieceId(id))]['desc']
    evols = getPieceFullEvolutionMapping(id)
    if id != evols[0]:
        template_args['pre-evolution'] = getPieceName(evols[evols.index(id) - 1])
    if id != evols[-1]:
        template_args['evolution'] = getPieceName(evols[evols.index(id) + 1])
    return generateGeneralMediaWikiTemplate('Clothing Infobox', template_args)

def generateLeadingClothing(id):
    return generateGeneralMediaWikiTemplate('Lead/Clothing', {'1': getPieceName(id)})

def GetRankName(score):
    for rank, rank_data in clothes_attribute_rank_table.items():
        if score >= rank_data['lowest_score'] and score < rank_data['highest_score']:
            return rank_data['level']
    return 'Unknown'

def generateScore(id):
    template_args = {}
    item = item_table[str(id)]
    extra = item_extra_table.get(str(id), {})
    styles = ['elegant', 'fresh', 'sweet', 'sexy', 'cool']
    rate_suffix = '_rate'
    max_rate_suffix = '_max_rate'
    for style in styles:
        template_args[style] = extra['cloth_props'][styles.index(style)]
        coeff = clothes_attribute_factor_table[str(item['minor_type'])]['coefficient'] / 100
        template_args[style + rate_suffix] = GetRankName(template_args[style] / coeff)
        # template_args[style + max_rate_suffix] = GetRankName(math.ceil(template_args[style] * 6.2) / coeff)
    return generateGeneralMediaWikiTemplate('Score', template_args)

def getNPCName(id):
    return character_table[str(id)]['name'] \
        .replace('NSLOCTEXT(', '') \
        .replace(')', '') \
        .replace('"', '') \
        .split(', ') \
        [2]

def generateComments(id):
    template_args = {}
    extra = item_extra_table.get(str(id), {})
    if str(extra['npc1']) not in character_table:
        return ''
    template_args['comment_1'] = extra['comment1']
    template_args['user_1'] = getNPCName(str(extra['npc1']))
    template_args['comment_2'] = extra['comment2']
    template_args['user_2'] = getNPCName(str(extra['npc2']))
    return generateGeneralMediaWikiTemplate('Comments', template_args)

def generateRecipe(id):
    template_args = {}
    template_args['type'] = 'Crafting'
    sketch = suit_formula_table[str(getSketchIdFromPieceId(id))]
    sort = []
    for item in sketch['material_consume']['item_list']:
        template_args[item_table[str(item['item_id'])]['name']] = item['amount']
        sort.append(item_table[str(item['item_id'])]['name'])
    template_args['sort'] = ';'.join(sort)
    return generateGeneralMediaWikiTemplate('Recipe', template_args)

from ol import LOCALES, LOCALE_REPLACE

def generateOL(id):
    template_args = {}

    key = item_table[str(id)]['name']

    with open(f'ol/Game_zh.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1].strip() == key:
                key = row[0]
                break

    for locale in LOCALES:
        with open(f'ol/Game_{locale}.csv', 'r', encoding='utf-8') as f:
            locale = LOCALE_REPLACE[locale]
            template_args[locale] = ''
            reader = csv.reader(f)
            for row in reader:
                if row[0] == key:
                    template_args[locale] = row[1].strip()
                    break

    return generateGeneralMediaWikiTemplate('Other Languages', template_args)

STRING_TABLE_PATH = r'D:\Program Files\FModel\Output\Exports\X6Game\Content\Config\Localization\StringTable_Excel.json'

with open(STRING_TABLE_PATH, 'r', encoding='utf-8') as f:
    string_table = json.load(f)

version_map = {
    '0.9.0': '0.9',
    '1.0.0': '1.0',
    '1.0.1': '1.0',
    '1.0.2': '1.0',
    '1.1.0': '1.1',
    '1.1.1': '1.1',
    '1.1.2': '1.1',
    '1.1.3': '1.1',
}

def generateChangeHistory(id):
    template_args = {}
    item = item_table[str(id)]
    key = item['l10nname']
    keys_to_metadata = string_table[0]['StringTable']['KeysToMetaData']
    version = version_map[keys_to_metadata[key]['X6VersionTag']]
    if version == '0.9':
        template_args['1'] = '1.0'
        template_args['introduced'] = '0.9'
    else:
        template_args['1'] = version
    return generateGeneralMediaWikiTemplate('Change History', template_args)

def generateOutfitPiecesNavbox(id):
    template_args = {}
    if id not in piece_to_suit_mapping:
        return ''
    template_args['1'] = getSuitName(getSuitIdFromPieceId(id))
    return generateGeneralMediaWikiTemplate('Outfit Pieces Navbox', template_args)

def generateClothingNavbox(id):
    template_args = {}
    template_args['1'] = getClothesMinorTypeName(item_table[str(id)]['minor_type'])
    return generateGeneralMediaWikiTemplate('Clothing Navbox', template_args)

def generateWardrobeNavbox(id):
    template_args = {}
    return generateGeneralMediaWikiTemplate('Wardrobe Navbox', template_args)

def generateInterwikiLinks(id):
    available_langs = ['en', 'fr']
    text = ''
    for lang in available_langs:
        with open(f'ol/Game_{lang}.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == '/' + item_table[str(id)]['l10nname']:
                    text += f'[[{lang}:{row[1]}]]\n'
                    break
    return text


def generatePieceWikitext(id):
    piece_wikitext = ''
    if len(getPieceFullEvolutionMapping(id)) > 1:
        piece_wikitext += generateEvolutionTabs(id) + '\n'
    piece_wikitext += generateClothingInfobox(id) + '\n'
    piece_wikitext += generateLeadingClothing(id) + '\n'
    piece_wikitext += '\n==评分==\n'
    piece_wikitext += generateScore(id) + '\n'
    comment = generateComments(id)
    if comment:
        piece_wikitext += '\n==评论==\n'
        piece_wikitext += generateComments(id) + '\n'
    if getSketchIdFromPieceId(id):
        piece_wikitext += '\n==制作材料==\n'
        piece_wikitext += generateRecipe(id) + '\n'
    piece_wikitext += '\n==其他语言==\n'
    piece_wikitext += generateOL(id) + '\n'
    piece_wikitext += '\n==变更历史==\n'
    piece_wikitext += generateChangeHistory(id) + '\n'
    piece_wikitext += '\n==导航==\n'
    piece_wikitext += generateOutfitPiecesNavbox(id) + '\n'
    piece_wikitext += generateClothingNavbox(id) + '\n'
    piece_wikitext += generateWardrobeNavbox(id) + '\n'
    piece_wikitext += '\n' + generateInterwikiLinks(id) + '\n'
    return piece_wikitext

def generate():
    os.makedirs('wikitext/pieces', exist_ok=True)
    for piece_id in item_table:
        print(piece_id)
        if item_table[piece_id]['major_type'] == 2:
            with open(f'wikitext/pieces/{getPieceName(piece_id).replace('*', '')}.wikitext', 'w', encoding='utf-8') as f:
                f.write(generatePieceWikitext(int(piece_id)))

def generateInterwikis():
    os.makedirs('wikitext/pieces/interwiki', exist_ok=True)
    for piece_id in item_table:
        print(piece_id)
        if item_table[piece_id]['major_type'] == 2:
            with open(f'wikitext/pieces/interwiki/{getPieceName(piece_id).replace('*', '')}.txt', 'w', encoding='utf-8') as f:
                f.write(generateInterwikiLinks(int(piece_id)))

if __name__ == '__main__':
    print(getPieceFullEvolutionMapping(1020100004))
    print(generateEvolutionTabs(1020100004))
    print(generateClothingInfobox(1020100004))
    print(generateLeadingClothing(1020100004))
    print(generateScore(1020100004))
    print(generateComments(1020100004))
    # print(generateRecipe(1020100004))
    print(generateOL(1020900126))
    print(generateChangeHistory(1020100004))
    print(generateOutfitPiecesNavbox(1020100004))
    print(generateClothingNavbox(1020100004))
    print(generateWardrobeNavbox(1020100004))
    print(generateInterwikiLinks(1020100004))
    print(generatePieceWikitext(1020100004))

    # generateInterwikis()
    # generate()

    import rename_images
    # rename_images.renamePiecesImages()

    import upload_wikitext
    # upload_wikitext.upload('pieces', '单品')