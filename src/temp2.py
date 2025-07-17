import shlex
import shutil
import os
import json
import csv
import subprocess


with open(r'cfg/config_output/item/TbItem.json', 'r', encoding='utf-8') as f:
    item_table = json.load(f)

with open(r'cfg/config_output/item/TbItemExtra.json', 'r', encoding='utf-8') as f:
    item_extra_table = json.load(f)

def changeQuality():
    for item_id, item in item_table.items():
        if item['major_type'] == 2:
            extra = item_extra_table.get(item_id, {})
            if item['quality'] != extra['clothers_quality'] and item['name'].startswith('**'):
                item_name = item['name'].replace('**', '')
                print(item_id, item['name'], item['quality'], extra['clothers_quality'])
                subprocess.run(
                    ['python', 'pwb.py', 'replace', f'-page:{item_name}', f'-summary:Bot：自动替换文本 (-"rarity={extra['clothers_quality']}" +"rarity={item['quality']}")', f'rarity={extra['clothers_quality']}', f'rarity={item['quality']}', '-always', '-sleep:0.1'], shell=True,
                    cwd=r"E:\nikki-wiki-bot\core_stable")

def AddGalleryScore():
    subprocess.run(['python', 'pwb.py', 'login'], shell=True, cwd=r"E:\nikki-wiki-bot\core_stable")
    for item_id, item in item_table.items():
        if item['major_type'] == 2:
            if item['gallery_score'] != 0:
                item_name = item['name'].replace('**', '')
                print(item_id, item['name'], item['quality'], item['gallery_score'])
                print(shlex.join(['python', 'pwb.py', 'replace', f'|rarity', f"|compendium_score={item['gallery_score']}\\n|rarity", f'-page:{item_name}', f'-summary:Bot：添加图鉴评价分+{item['gallery_score']}', '-excepttext:compendium_score', '-always', '-sleep:0.1']))
                subprocess.run(
                    ['python', 'pwb.py', 'replace', f'|rarity', f'|compendium_score={item['gallery_score']}\\n|rarity', f'-page:{item_name}', f'-summary:Bot：添加图鉴评价分+{item['gallery_score']}', '-excepttext:compendium_score', '-always', '-sleep:0.1'],
                    cwd=r"E:\nikki-wiki-bot\core_stable")

def addInterwiki():
    for root, dirs, files in os.walk(r'E:\perfect\src\wikitext\pieces\interwiki'):
        for file in files:
            path = root.replace("\\", "/") + "/" + file
            filename = os.path.basename(file).replace(".txt", "")
            subprocess.run(
                ['python', 'pwb.py', 'interwiki', f'-start:{filename}', f'-number:1',
                 f'-hintfile:{path}', '-hintsareright', '-force'], shell=True,
                cwd=r"E:\nikki-wiki-bot\core_stable")

# addInterwiki()
AddGalleryScore()