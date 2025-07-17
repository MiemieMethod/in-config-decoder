import csv
import os
import subprocess

I_N_DATA_PATH = r'D:\工作区\I-N-Data' # Change here to your path, where X6Game/../.locres files located, maybe your path/to/fmodel/Output/Exports

LOCALES = [
    'zh',
    'zh-Hant',
    # 'zh-SG', # Singapore Chinese is actually the same as Simplified Chinese
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

LOCALE_REPLACE = {
    'zh': 'zhs',
    'zh-Hant': 'zht',
    # 'zh-SG': 'zh-Hans',
    'en': 'en',
    'ja-JP': 'ja',
    'ko': 'ko',
    'th': 'th',
    'id': 'id',
    'pt': 'pt',
    'es': 'es',
    'fr': 'fr',
    'de': 'de',
    'it': 'it',
}

def decodeLocres():
    os.makedirs('ol', exist_ok=True)
    for locale in LOCALES:
        subprocess.run(['./UnrealLocres', 'export', os.path.join(I_N_DATA_PATH, f'X6Game/Content/Localization/Game/{locale}/Game.locres'), '-f', 'csv', '-o', f'ol/Game_{locale}.csv'], encoding='utf-8')

def generateGeneralMediaWikiTemplate(name, args: dict, save_at: str = ''):
    template = f'{{{{{name}\n'
    for key, value in args.items():
        template += f'|{key}={value}\n'
    template += '}}'
    print(template)
    if save_at:
        with open(save_at, 'w', encoding='utf-8') as f:
            f.write(template)
    return template

def generateOL(key_or_name: int|str, your_locale: str = 'en'):
    args_dict = {}

    key = str(key_or_name)
    with open(f'ol/Game_{your_locale}.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == key_or_name:
                key = row[0]
                break

    for locale in LOCALES:
        with open(f'ol/Game_{locale}.csv', 'r', encoding='utf-8') as f:
            locale = LOCALE_REPLACE[locale]
            args_dict[locale] = ''
            reader = csv.reader(f)
            for row in reader:
                if row[0] == key:
                    args_dict[locale] = row[1]
                    break

    return generateGeneralMediaWikiTemplate('Other Languages', args_dict, f'ol/output.wikitext')


if __name__ == '__main__':
    I_WANT_TO_GENERATE = 'Mortal Waters' # Can be key or name, key should be formatted like '/Key' (root namespace) or 'Namespace/Key'

    decodeLocres()
    generateOL(I_WANT_TO_GENERATE)

    # I_WANT_TO_GENERATE = '愤怒石头人'
    # generateOL(I_WANT_TO_GENERATE, 'zh') # You can specify your locale here, default is 'en'
