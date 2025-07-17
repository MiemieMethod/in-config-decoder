from post_process import *
import difflib

OLD_FOLDER = '1.5.2'

def loadJson(file: str):
    with open(file, 'r', encoding='utf-8') as f:
        return json.load(f)

def loadCsv(file: str):
    with open(file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        result = {}
        for row in reader:
            result[row['key'][1:]] = row['source']
        return result


def diffFiles(file1_path, file2_path):
    with open(file1_path, 'r', encoding='utf-8') as file1:
        file1_lines = file1.readlines()

    with open(file2_path, 'r', encoding='utf-8') as file2:
        file2_lines = file2.readlines()

    diff = difflib.unified_diff(
        file1_lines, file2_lines,
        fromfile='file1', tofile='file2',
        lineterm=''
    )

    for line in diff:
        print(line)

'''
the new dict may have more keys than the old dict, vice versa, we only need to compare the keys that are in both dicts
:return 0 if equal, 1 if different
'''
def diffDict(old: dict, new: dict):
    for key, value in old.items():
        if key in new:
            if value != new[key]:
                return 1
    return 0

def generateAddChangeRemove(file):
    old = loadJson(f'cfg/{OLD_FOLDER}/{file}.json')
    new = loadJson(f'cfg/{file}.json')
    old_text = loadCsv(f'cfg/{OLD_FOLDER}/Game_{LOCALE}.csv')
    added = []
    changed = []
    removed = []
    for key, value in new.items():
        if key in old:
            if diffDict(old[key], value):
                changed.append(key)
        else:
            added.append(key)
    for key in old:
        if key not in new:
            removed.append(key)
    return old, new, old_text, added, changed, removed

def diffItems():
    old, new, old_text, added, changed, removed = generateAddChangeRemove('item.TbItem')

    # format: Added: \n key1: name1 \n key2: name2 \n\n Changed: \n key3: name3 \n key4: name4 \n\n Removed: \n key5: name5 \n key6: name6
    simpleDiffList = 'Added: \n'
    for key in added:
        simpleDiffList += f'{key}: {texts.get(new[key]['NameKey'], new[key]['NameKey'])}\n'
    simpleDiffList += '\nChanged: \n'
    for key in changed:
        simpleDiffList += f'{key}: {texts.get(new[key]['NameKey'], new[key]['NameKey'])}\n'
    simpleDiffList += '\nRemoved: \n'
    for key in removed:
        simpleDiffList += f'{key}: {old_text.get(old[key]['NameKey'], old[key]['NameKey'])}\n'
    with open('cfg/diff_item.txt', 'w', encoding='utf-8') as f:
        f.write(simpleDiffList)

    detailDiffList = '==== Added ====\n'
    for key in added:
        detailDiffList += genSingleItem(key)
    detailDiffList += '==== Changed ====\n'
    for key in changed:
        detailDiffList += 'Old:\n'
        detailDiffList += genSingleItem(key, old[key])
        detailDiffList += 'New:\n'
        detailDiffList += genSingleItem(key)
    detailDiffList += '==== Removed ====\n'
    for key in removed:
        detailDiffList += genSingleItem(key, old[key])
    with open('cfg/diff_item_detail.txt', 'w', encoding='utf-8') as f:
        f.write(detailDiffList)

def diffPieces():
    old, new, old_text, added, changed, removed = generateAddChangeRemove('item.TbItemExtra')

    old_item = loadJson(f'cfg/{OLD_FOLDER}/item.TbItem.json')
    new_item = loadJson(f'cfg/item.TbItem.json')

    simpleDiffList = 'Added: \n'
    for key in added:
        if key in new_item:
            simpleDiffList += f'{key}: {texts.get(new_item[key]['NameKey'], new_item[key]['NameKey'])}\n'
    simpleDiffList += '\nChanged: \n'
    for key in changed:
        simpleDiffList += f'{key}: {texts.get(new_item[key]['NameKey'], new_item[key]['NameKey'])}\n'
    simpleDiffList += '\nRemoved: \n'
    for key in removed:
        simpleDiffList += f'{key}: {old_text.get(old_item[key]['NameKey'], old_item[key]['NameKey'])}\n'
    with open('cfg/diff_piece.txt', 'w', encoding='utf-8') as f:
        f.write(simpleDiffList)

    detailDiffList = '==== Added ====\n'
    for key in added:
        detailDiffList += genSinglePiece(key)
    detailDiffList += '==== Changed ====\n'
    for key in changed:
        detailDiffList += 'Old:\n'
        detailDiffList += genSinglePiece(key, old[key])
        detailDiffList += 'New:\n'
        detailDiffList += genSinglePiece(key)
    detailDiffList += '==== Removed ====\n'
    for key in removed:
        detailDiffList += genSinglePiece(key, old[key])
    with open('cfg/diff_piece_detail.txt', 'w', encoding='utf-8') as f:
        f.write(detailDiffList)

def diffSuits():
    old, new, old_text, added, changed, removed = generateAddChangeRemove('clothes.TbSuit')

    simpleDiffList = 'Added: \n'
    for key in added:
        simpleDiffList += f'{key}: {texts.get(new[key]['NameKey'], new[key]['NameKey'])}\n'
    simpleDiffList += '\nChanged: \n'
    for key in changed:
        simpleDiffList += f'{key}: {texts.get(new[key]['NameKey'], new[key]['NameKey'])}\n'
    simpleDiffList += '\nRemoved: \n'
    for key in removed:
        simpleDiffList += f'{key}: {old_text.get(old[key]['NameKey'], old[key]['NameKey'])}\n'
    with open('cfg/diff_suit.txt', 'w', encoding='utf-8') as f:
        f.write(simpleDiffList)

    detailDiffList = '==== Added ====\n'
    for key in added:
        detailDiffList += genSingleSuit(key)
    detailDiffList += '==== Changed ====\n'
    for key in changed:
        detailDiffList += 'Old:\n'
        detailDiffList += genSingleSuit(key, old[key])
        detailDiffList += 'New:\n'
        detailDiffList += genSingleSuit(key)
    detailDiffList += '==== Removed ====\n'
    for key in removed:
        detailDiffList += genSingleSuit(key, old[key])
    with open('cfg/diff_suit_detail.txt', 'w', encoding='utf-8') as f:
        f.write(detailDiffList)

def diffMagicBalls():
    old, new, old_text, added, changed, removed = generateAddChangeRemove('magic_ball.TbMagicBallInfo')

    old_item = loadJson(f'cfg/{OLD_FOLDER}/item.TbItem.json')
    new_item = loadJson(f'cfg/item.TbItem.json')

    simpleDiffList = 'Added: \n'
    for key in added:
        simpleDiffList += f'{key}: {texts.get(new_item[key]['NameKey'], new_item[key]['NameKey'])}\n'
    simpleDiffList += '\nChanged: \n'
    for key in changed:
        simpleDiffList += f'{key}: {texts.get(new_item[key]['NameKey'], new_item[key]['NameKey'])}\n'
    simpleDiffList += '\nRemoved: \n'
    for key in removed:
        simpleDiffList += f'{key}: {old_text.get(old_item[key]['NameKey'], old_item[key]['NameKey'])}\n'
    with open('cfg/diff_magic_ball.txt', 'w', encoding='utf-8') as f:
        f.write(simpleDiffList)

    detailDiffList = '==== Added ====\n'
    for key in added:
        detailDiffList += genSingleMagicBall(key)
    detailDiffList += '==== Changed ====\n'
    for key in changed:
        detailDiffList += 'Old:\n'
        detailDiffList += genSingleMagicBall(key, old[key])
        detailDiffList += 'New:\n'
        detailDiffList += genSingleMagicBall(key)
    detailDiffList += '==== Removed ====\n'
    for key in removed:
        detailDiffList += genSingleMagicBall(key, old[key])
    with open('cfg/diff_magic_ball_detail.txt', 'w', encoding='utf-8') as f:
        f.write(detailDiffList)


def diff():
    diffItems()
    diffPieces()
    diffSuits()
    diffMagicBalls()