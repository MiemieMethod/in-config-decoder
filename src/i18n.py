import csv
import json
import os
import re
import subprocess

LOCALES = [
    'zh',
    'zh-Hant',
    'zh-SG', # Singapore Chinese is actually the same as Simplified Chinese
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

def decode_locres(I_N_DATA_PATH):
    os.makedirs('ol', exist_ok=True)
    for locale in LOCALES:
        os.makedirs(f'cfg/repo/TextMap/{locale}', exist_ok=True)
        subprocess.run(['./UnrealLocres', 'export', os.path.join(I_N_DATA_PATH, f'X6Game/Content/Localization/Game/{locale}/Game.locres'), '-f', 'csv', '-o', f'cfg/repo/TextMap/{locale}/Game.csv'], encoding='utf-8')
        csv_path = f'cfg/repo/TextMap/{locale}/Game.csv'
        with open(csv_path, 'rb') as f:
            content = f.read().decode('utf-8')
        content = re.sub(r',([^"\s]*?\r[^"\s]*?),', r',"$1",', content)
        with open(csv_path, 'wb') as f:
            f.write(content.encode('utf-8'))
        textmap = {}
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == 'key':
                    continue
                split = row[0].split('/')
                namespace, key = split
                if namespace not in textmap:
                    textmap[namespace] = {}
                textmap[namespace][key] = row[1]
        with open(f'cfg/repo/TextMap/{locale}/Game.json', 'w', encoding='utf-8') as w:
            json.dump(textmap, w, ensure_ascii=False, indent=2)
        os.remove(f'cfg/repo/TextMap/{locale}/Game.csv')

