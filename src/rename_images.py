import shutil
import os
import json
import csv

with open(r'cfg/config_output/item/TbItem.json', 'r', encoding='utf-8') as f:
    item_table = json.load(f)

with open(r'cfg/config_output/item/TbItemExtra.json', 'r', encoding='utf-8') as f:
    item_extra_table = json.load(f)

en_texts = {}
with open(f'cfg/Game_en.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        en_texts[row['key']] = row['source']

def getEnText(key):
    return en_texts.get('/' + key, '')

def getPieceName(piece_id):
    return item_table[str(piece_id)]['name']

def getPieceEnName(piece_id):
    piece = item_table[str(piece_id)]
    return getEnText(piece['l10nname'])

def resolveImagePath(path, newest_splitted_images_path):
    return path.split("'")[1].split(".")[0].replace('/Game', newest_splitted_images_path) + '.png'

def resolveAsFallbackImagePath(path, fall_back_images_path):
    return path.split("'")[1].split(".")[0].replace('/Game', fall_back_images_path) + '.png'

def renamePiecesImages():
    os.makedirs('wikitext/pieces/images', exist_ok=True)
    newest_splitted_images_path = r'E:\I-N-wwise-extractor\output\image'
    fall_back_images_path = r'E:\I-N-Images\X6Game\Content'
    for item_id, item in item_table.items():
        if item['major_type'] == 2:
            icon_name = resolveImagePath(item['icon'], newest_splitted_images_path)
            extra = item_extra_table.get(item_id, {})
            showpic_name = resolveImagePath(extra['clothes_showpic'], newest_splitted_images_path)
            name = getPieceEnName(int(item_id)) if getPieceEnName(int(item_id)) else getPieceName(int(item_id)).replace('*', '')
            if os.path.exists(icon_name):
                shutil.copy2(icon_name, f'wikitext/pieces/images/{name} Icon.png')
            else:
                fall_back_path = resolveAsFallbackImagePath(item['icon'], fall_back_images_path)
                if os.path.exists(fall_back_path):
                    shutil.copy2(fall_back_path, f'wikitext/pieces/images/{name} Icon.png')
                else:
                    print(f'Icon not found for {getPieceName(int(item_id))}')
            if os.path.exists(showpic_name):
                shutil.copy2(showpic_name, f'wikitext/pieces/images/{name} Showpic.png')
            else:
                fall_back_path = resolveAsFallbackImagePath(extra['clothes_showpic'], fall_back_images_path)
                if os.path.exists(fall_back_path):
                    shutil.copy2(fall_back_path, f'wikitext/pieces/images/{getPieceEnName(int(item_id))} Showpic.png')
                else:
                    print(f'Showpic not found for {getPieceName(int(item_id))}')

if __name__ == '__main__':
    renamePiecesImages()