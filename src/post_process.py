import csv
import json
import re
from math import ceil
import os
import subprocess

LOCALE = 'zh'
SIMPLE = True

I_N_CONFIGS_PATH = r'D:\Program Files\FModel\Output\Exports' # change here to your path

DECODED_CONFIGS_PATH = r'cfg/config_output'

with open(r'cfg/config_output/item/TbItem.json', 'r', encoding='utf-8') as f:
    item_table = json.load(f)

with open(r'cfg/config_output/item/TbItemExtra.json', 'r', encoding='utf-8') as f:
    item_extra_table = json.load(f)

with open(r'cfg/config_output/clothes/TbClothesAttributeFactor.json', 'r', encoding='utf-8') as f:
    clothes_attribute_factor_table = json.load(f)

with open(r'cfg/config_output/clothes/TbClothesAttributeRank.json', 'r', encoding='utf-8') as f:
    clothes_attribute_rank_table = json.load(f)

with open(r'cfg/config_output/character/TbCharacterInfo.json', 'r', encoding='utf-8') as f:
    character_table = json.load(f)

texts = {}
en_texts = {}
item_extra = {}
item = {}
character_info = {}
suit = {}
factors = {}
ranks = {}
display_type = {}
tags = {}
obtains = {}
level = {}
renew = {}
formulas = {}
magic_ball = {}
magic_ball_level = {}
dialogue = {}
dialogue_line = {}
dialogue_temp_name = {}
dialogue_choice = {}
character_info2 = {}
gameplay_tags = {}
graph_nodes = {}
graph_quest_datas = {}
missions = {}
quest_first_objective = {}
scene_obj = {}
world = {}
cutscene ={}

def loadConfigs():
    global texts, item_extra, item, character_info, suit, factors, ranks, display_type, tags, obtains, level, renew, formulas, magic_ball, magic_ball_level, dialogue, dialogue_line, dialogue_temp_name, dialogue_choice, character_info2, gameplay_tags, graph_nodes, graph_quest_datas, missions, quest_first_objective, scene_obj, world, cutscene

    with open(f'cfg/Game_{LOCALE}.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            texts[row['key']] = row['source']

    with open(f'cfg/Game_en.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            en_texts[row['key']] = row['source']

    with open('cfg/item.TbItemExtra.json', 'r', encoding='utf-8') as f:
        item_extra = json.load(f)

    with open('cfg/item.TbItem.json', 'r', encoding='utf-8') as f:
        item = json.load(f)

    with open('cfg/character.TbCharacterInfo.json', 'r', encoding='utf-8') as f:
        character_info = json.load(f)

    with open('cfg/clothes.TbSuit.json', 'r', encoding='utf-8') as f:
        suit = json.load(f)

    with open('cfg/clothes.TbClothesAttributeFactor.json', 'r', encoding='utf-8') as f:
        factors = json.load(f)

    with open('cfg/clothes.TbClothesAttributeRank.json', 'r', encoding='utf-8') as f:
        ranks = json.load(f)

    with open('cfg/item.TbDisplayTypeInfo.json', 'r', encoding='utf-8') as f:
        display_type = json.load(f)

    with open('cfg/clothes.TbClothersTagInfo.json', 'r', encoding='utf-8') as f:
        tags = json.load(f)

    with open('cfg/gallery.TbGalleryObtainMethod.json', 'r', encoding='utf-8') as f:
        obtains = json.load(f)

    with open('cfg/clothes.TbClothesLevelNormalInfo.json', 'r', encoding='utf-8') as f:
        level = json.load(f)

    with open('cfg/clothes.TbClothesRenewNormalInfo.json', 'r', encoding='utf-8') as f:
        renew = json.load(f)

    with open('cfg/clothes.TbSuitFormula.json', 'r', encoding='utf-8') as f:
        formulas = json.load(f)

    with open('cfg/magic_ball.TbMagicBallInfo.json', 'r', encoding='utf-8') as f:
        magic_ball = json.load(f)

    with open('cfg/magic_ball.TbBallLevelUpInfo.json', 'r', encoding='utf-8') as f:
        magic_ball_level = json.load(f)

    with open(os.path.join(DECODED_CONFIGS_PATH, r'dialogue/TbDialogueListV3.json'), 'r', encoding='utf-8') as f:
        dialogue = json.load(f)

    with open(os.path.join(DECODED_CONFIGS_PATH, r'dialogue/TbDialogueLineInfo.json'), 'r', encoding='utf-8') as f:
        dialogue_line = json.load(f)

    with open(os.path.join(DECODED_CONFIGS_PATH, r'dialogue/TbDialogueTempNameInfo.json'), 'r', encoding='utf-8') as f:
        dialogue_temp_name = json.load(f)

    with open(os.path.join(DECODED_CONFIGS_PATH, r'dialoguechoice/Tb_DT_ChoiceLineList.json'), 'r', encoding='utf-8') as f:
        dialogue_choice = json.load(f)

    with open(os.path.join(DECODED_CONFIGS_PATH, r'character/TbCharacterInfo.json'), 'r', encoding='utf-8') as f:
        character_info2 = json.load(f)

    with open(os.path.join(DECODED_CONFIGS_PATH, r'gameplaytags/TbGameplayTagInfo.json'), 'r', encoding='utf-8') as f:
        gameplay_tags = json.load(f)

    with open(os.path.join(DECODED_CONFIGS_PATH, r'graph/TbGraphNodeData.json'), 'r', encoding='utf-8') as f:
        graph_nodes = json.load(f)

    with open(os.path.join(DECODED_CONFIGS_PATH, r'graph/TbGraphQuestDatas.json'), 'r', encoding='utf-8') as f:
        graph_quest_datas = json.load(f)

    with open(os.path.join(DECODED_CONFIGS_PATH, r'mission/Tb_DT_Mission.json'), 'r', encoding='utf-8') as f:
        missions = json.load(f)

    with open(os.path.join(DECODED_CONFIGS_PATH, r'mission/TbQuestFirstObjectiveInfo.json'), 'r', encoding='utf-8') as f:
        quest_first_objective = json.load(f)

    with open(os.path.join(DECODED_CONFIGS_PATH, r'obj/TbSceneObj.json'), 'r', encoding='utf-8') as f:
        scene_obj = json.load(f)

    with open(os.path.join(DECODED_CONFIGS_PATH, r'map/TbWorldV2.json'), 'r', encoding='utf-8') as f:
        world = json.load(f)

    with open(os.path.join(DECODED_CONFIGS_PATH, r'cutscene/TbCutSceneAnchor.json'), 'r', encoding='utf-8') as f:
        cutscene = json.load(f)



def getText(key, fallback, namespace = ''):
    return texts.get(f'{namespace}/{key}', fallback)

def getEnText(key, fallback, namespace = ''):
    return en_texts.get(f'{namespace}/{key}', fallback)

def getNSLOCTEXT(text):
    splitted = text.replace("NSLOCTEXT(", '').replace(")", '').replace("\"", '').split(', ')
    if len(splitted) != 3:
        return 'Unknown'
    namespace = splitted[0]
    key = splitted[1]
    name = splitted[2]
    if getText(key, '') == '':
        return getText(key, name, namespace)
    else:
        return getText(key, name, '')

def getCharacterName2(id):
    if str(id) not in character_info2:
        return f'Character_{id}'
    char = character_info2[str(id)]
    return getNSLOCTEXT(char['name'])

character_tag_to_char_map = {}

def buildCharacterTagToCharMap():
    for char_id, char in character_info2.items():
        tag = char['character_tag']
        if str(tag) in gameplay_tags:
            name = getCharacterName2(char_id)
            character_tag_to_char_map[gameplay_tags[str(tag)]['EnumName']] = name
            character_tag_to_char_map[gameplay_tags[str(tag)]['EnumAlias']] = name
    for obj_id, obj in scene_obj.items():
        tag = obj['obj_tag']
        if str(tag) in gameplay_tags:
            name = getText(obj['l10ncomp_name'], obj['comp_name'])
            character_tag_to_char_map[gameplay_tags[str(tag)]['EnumName']] = name
            character_tag_to_char_map[gameplay_tags[str(tag)]['EnumAlias']] = name

next_dlg_stage_to_choice = {}

def buildNextDlgStageToChoiceMap():
    for choice_id, choice in dialogue_choice.items():
        next_dlg_stage_to_choice[choice['NextDlgStage']] = getNSLOCTEXT(choice['ChoiceLineString'])

dialogue_uid_to_node = {}

def buildDialogueUidToNodeMap():
    for node_id, node in graph_nodes.items():
        if node['asset_type'] == 'DialogueStage':
            dialogue_uid_to_node[node['asset_target_id']] = node_id
            dialogue_uid_to_node[int(node['asset_id'])] = node_id
        elif node['asset_type'] == 'dialog_uid':
            dialogue_uid_to_node[int(node['asset_id'])] = node_id

dlg_stage_to_char = {}

def buildDlgStageToCharMap():
    for character_id, character in character_info2.items():
        dlg_stage_to_char[character['dialogue_stage']] = getCharacterName2(character_id)

mission_tag_to_name = {}

def buildMissionTagToNameMap():
    for mission_id, mission in missions.items():
        mission_tag_to_name[mission['mission_tag']] = getNSLOCTEXT(mission['name'])

def genSingleDialogue(dialogue_id, _dialogue=None):
    if not _dialogue:
        _dialogue = dialogue[dialogue_id]
    text = f'======= {_dialogue["Name"]} ========\n'
    text += f'UID: {_dialogue["DialogueUid"]}\n'
    if _dialogue['DialogueStage'] in next_dlg_stage_to_choice:
        choice_text = next_dlg_stage_to_choice[_dialogue["DialogueStage"]]
        text += f'Choice: {choice_text}\n'
    if _dialogue['DialogueStage'] in dlg_stage_to_char:
        text += f'Character: {dlg_stage_to_char[_dialogue["DialogueStage"]]}\n'
    if int(dialogue_id) in dialogue_uid_to_node:
        graph_node_id = dialogue_uid_to_node[int(dialogue_id)]
        graph_id = graph_nodes[graph_node_id]['graph_id']
        if str(graph_id) in graph_quest_datas:
            quests = graph_quest_datas[str(graph_id)]['quest_ids']
            quest_strings = []
            for quest in quests:
                if str(quest) in missions:
                    mission_name = getNSLOCTEXT(missions[str(quest)]['name'])
                else:
                    mission_name = quest_first_objective[str(quest)]['quest_tag']
                quest_strings.append(mission_name)
            text += f'Quest: {", ".join(quest_strings)}\n'
        else:
            text += f'Quest: {graph_nodes[graph_node_id]["graph_name"]}\n'
    else:
        guess_name = ''
        split_id = _dialogue["Name"].split('_')
        if _dialogue['Name'].startswith('q'):
            if len(split_id) == 3:
                guess_name = 'MS_' + split_id[0]
            else:
                guess_name = 'MS_' + split_id[0].replace('q', '') + '_' + split_id[1]
        if _dialogue['Name'].startswith('evt'):
            guess_name = 'EV_' + split_id[0].replace('evt', '')
        if guess_name in mission_tag_to_name:
            text += f'Quest: {mission_tag_to_name[guess_name]}\n'
        if _dialogue['Name'].startswith('s'):
            guess_name = split_id[0].replace('s', '')
        if guess_name in world:
            text += f'Scene: {getText(world[guess_name]["l10n_name"], world[guess_name]["name"])}\n'
    if _dialogue['DialogueStage'].startswith('/Game/'):
        stage = _dialogue["DialogueStage"].split('.')[0].replace('/Game/', '/X6Game/Content/') + '.json'
    else:
        stage = r'\X6Game\Plugins\GameFeatures' + _dialogue["DialogueStage"].split('.')[0].replace('/Assets/', '/Content/Assets/') + '.json'
    stage_path = I_N_CONFIGS_PATH + stage
    if not os.path.exists(stage_path):
        print(f'DialogueStage File not found: {stage_path}')
        return text
    with open(stage_path, 'r', encoding='utf-8') as f:
        stage_content = json.load(f)
    for element in stage_content:
        if element['Type'] == 'PaperDialogue':
            text += f'==== {element["Outer"].replace("PaperDialogueNode_", "")}\n'
            actors = []
            if 'Actors' in element['Properties']:
                for a in element['Properties']['Actors']:
                    actors.append(character_tag_to_char_map.get(a['ActorName'], a['ActorName']))
                text += f'Actors: {", ".join(actors)}\n'
            for line in element['Properties']['Lines']:
                sep = "：'''" if LOCALE == 'zh' else ":''' "
                try_get_temp_name = dialogue_temp_name.get(str(line["Speaker"]['StringID']) + '_TempNTID', {})
                if try_get_temp_name:
                    char_name = getText(try_get_temp_name['l10ntemp_name'], try_get_temp_name['temp_name'])
                else:
                    char_name = character_tag_to_char_map.get(line["Speaker"]['ActorName'], line["Speaker"]['ActorName'])
                if line["Speaker"]['ActorName'] == 'None' and line["Speaker"]['StringID'] == 'None':
                    text += ';(Empty Dialogue Interval)\n' if LOCALE == 'en' else ';(空白间隔)\n'
                else:
                    text += f":'''{char_name}{sep}{getText('LDLG_Text_ZH_' + line['Speaker']['StringID'], line['Speaker']['StringID'])}\n"
            text += '\n'
        if element['Type'] == 'PaperDialogueMenu':
            text += f'==== {"Option" if LOCALE == "en" else "选项"} {element["Name"].replace("PaperDialogueMenu_", "")}\n'
            if 'Properties' in element and 'DialogueChoices' in element['Properties']:
                for choice in element['Properties']['DialogueChoices']:
                    text += f":'''{getText('LDLG_Text_ZH_' + choice['DialogueLineID'], choice['DialogueLineID'])}'''\n"
                text += '\n'
    text += '\n'
    replacements = {
        'RedBold': '{{{{Color|Pink|{}}}}}',
        'BlueBold': '{{{{Color|Blue|{}}}}}',
        'Italic': "''{}''",
        'RedBoldItalic': "{{{{Color|Pink|''{}''}}}}",
        'BlueBoldItalic': "{{{{Color|Blue|''{}''}}}}",
    }
    text = replaceTags(text, replacements)
    return text

def replaceTags(text, replacements):
    def replacement(match):
        tag = match.group(1)
        content = match.group(2)
        if tag in replacements:
            return replacements[tag].format(content)
        return match.group(0)

    # This regex matches tags like <Tag>content</>
    pattern = r'<(\w+)>(.*?)</>'
    return re.sub(pattern, replacement, text)

def generateDialogues():
    result = ""
    for dialogue_id in sorted(dialogue.keys(), key=lambda x: dialogue[x]['Name']):
        result += genSingleDialogue(dialogue_id)
    return result

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
    name = getText(name, f'Character_{id}')
    return name


def joinCharacter(arr):
    return ' & '.join([getCharacterName(i) for i in arr])


cutscene_uid_to_node = {}

def buildCutsceneUidToNodeMap():
    for node_id, node in graph_nodes.items():
        if node['asset_type'] == 'cutscene_asset':
            cutscene_uid_to_node[node['asset_id']] = node_id

def parseCutscene(id, name, path, start, is_sub = False):
    if is_sub:
        text = f'==== {name}\n'
    else:
        text = f'======= {name} ========\n'
    if id in cutscene_uid_to_node:
        graph_node_id = cutscene_uid_to_node[id]
        graph_id = graph_nodes[graph_node_id]['graph_id']
        if str(graph_id) in graph_quest_datas:
            quests = graph_quest_datas[str(graph_id)]['quest_ids']
            quest_strings = []
            for quest in quests:
                if str(quest) in missions:
                    mission_name = getNSLOCTEXT(missions[str(quest)]['name'])
                else:
                    mission_name = quest_first_objective[str(quest)]['quest_tag']
                quest_strings.append(mission_name)
            text += f'Quest: {", ".join(quest_strings)}\n'
        else:
            text += f'Quest: {graph_nodes[graph_node_id]["graph_name"]}\n'
    if path.startswith('/Game/'):
        stage = path.replace('/Game/', '/X6Game/Content/') + '.json'
    else:
        stage = r'\X6Game\Plugins\GameFeatures' + path.replace('/Assets/', '/Content/Assets/') + '.json'
    stage_path = I_N_CONFIGS_PATH + stage
    if not os.path.exists(stage_path):
        print(f'CutScene File not found: {stage_path}')
        return text
    with open(stage_path, 'r', encoding='utf-8') as f:
        stage_content = json.load(f)
    name_to_element = {}
    index_to_element = []
    for element in stage_content:
        name_to_element[element['Name']] = element
        index_to_element.append(element)
    if start in name_to_element:
        master = name_to_element[start]
    else:
        master = index_to_element[int(start)]
    # print(id)
    if 'Properties' not in master or 'MovieScene' not in master['Properties']:
        return text
    movie_scene = index_to_element[int(master['Properties']['MovieScene']['ObjectPath'].split('.')[1])]
    if 'Tracks' in movie_scene['Properties']:
        tracks = movie_scene['Properties']['Tracks']
        for track in tracks:
            name = track['ObjectName']
            path = track['ObjectPath']
            type = name.split("'")[0]
            index = path.split(".")[1]
            if type == 'MovieSceneCinematicShotTrack':
                track = index_to_element[int(index)]
                sections = track['Properties']['Sections']
                for section in sections:
                    section_name = section['ObjectName']
                    section_path = section['ObjectPath']
                    type = section_name.split("'")[0]
                    index = section_path.split(".")[1]
                    if type == 'MovieSceneCinematicShotSection':
                        section = index_to_element[int(index)]
                        subsequence = section['Properties']['SubSequence']
                        if subsequence is not None:
                            subsequence_name = subsequence['ObjectName']
                            subsequence_path = subsequence['ObjectPath']
                            type = subsequence_name.split("'")[0]
                            true_name = subsequence_name.split("'")[1]
                            true_path = subsequence_path.split(".")[0]
                            index = subsequence_path.split(".")[1]
                            if type == 'LevelSequence':
                                text += parseCutscene(subsequence_path, true_name, true_path, index, True)
            elif type == 'BP_SequencerLineTrack_C':
                track = index_to_element[int(index)]
                if 'Sections' not in track['Properties']:
                    text += ';(Empty Dialogue Interval)\n' if LOCALE == 'en' else ';(空白间隔)\n'
                else:
                    lines = track['Properties']['Sections']
                    for line in lines:
                        line_name = line['ObjectName']
                        line_path = line['ObjectPath']
                        type = line_name.split("'")[0]
                        index = line_path.split(".")[1]
                        if type == 'BP_SequencerLineSection_C':
                            line = index_to_element[int(index)]
                            if 'LineId[1]' not in line['Properties']:
                                text += ';(Empty Dialogue Interval)\n' if LOCALE == 'en' else ';(空白间隔)\n'
                            else:
                                line_id = line['Properties']['LineId[1]']
                                speaker = dialogue_line[line_id]['SpeakerTag'] if line_id in dialogue_line else 'None'
                                line_text = getText('LDLG_Text_ZH_' + line_id, 'None')
                                sep = "：'''" if LOCALE == 'zh' else ":''' "
                                try_get_temp_name = dialogue_temp_name.get(line_id + '_TempNTID', {})
                                if try_get_temp_name:
                                    char_name = getText(try_get_temp_name['l10ntemp_name'], try_get_temp_name['temp_name'])
                                else:
                                    char_name = character_tag_to_char_map.get(speaker, speaker)
                                if speaker == 'None' and line_text == 'None':
                                    text += ';(Empty Dialogue Interval)\n' if LOCALE == 'en' else ';(空白间隔)\n'
                                else:
                                    text += f":'''{char_name}{sep}{line_text}\n"
            elif type == 'BP_BlackScreenTextTrack_C':
                track = index_to_element[int(index)]
                if 'Sections' not in track['Properties']:
                    text += ';(Empty Black Screen)\n' if LOCALE == 'en' else ';(空白黑屏)\n'
                else:
                    lines = track['Properties']['Sections']
                    text += ';(Start Black Screen)\n' if LOCALE == 'en' else ';(开始黑屏)\n'
                    for line in lines:
                        line_name = line['ObjectName']
                        line_path = line['ObjectPath']
                        type = line_name.split("'")[0]
                        index = line_path.split(".")[1]
                        if type == 'BP_BlackScreenTextSection_C':
                            line = index_to_element[int(index)]
                            if 'TextLineID[1]' not in line['Properties']:
                                text += ';(Empty Black Screen)\n' if LOCALE == 'en' else ';(空白黑屏)\n'
                            else:
                                line_id = line['Properties']['TextLineID[1]']
                                speaker = dialogue_line[line_id]['SpeakerTag'] if line_id in dialogue_line else 'None'
                                line_text = getText('LDLG_Text_ZH_' + line_id, 'None')
                                sep = "：'''" if LOCALE == 'zh' else ":''' "
                                try_get_temp_name = dialogue_temp_name.get(line_id + '_TempNTID', {})
                                if try_get_temp_name:
                                    char_name = getText(try_get_temp_name['l10ntemp_name'], try_get_temp_name['temp_name'])
                                else:
                                    char_name = character_tag_to_char_map.get(speaker, speaker)
                                if speaker == 'None' and line_text == 'None':
                                    text += ';(Empty Black Screen)\n' if LOCALE == 'en' else ';(空白黑屏)\n'
                                else:
                                    text += f":'''{char_name}{sep}{line_text}\n"
                    text += ';(End Black Screen)\n' if LOCALE == 'en' else ';(结束黑屏)\n'
            elif type == 'MovieSceneSubTrack':
                track = index_to_element[int(index)]
                if 'Sections' in track['Properties']:
                    sections = track['Properties']['Sections']
                    for section in sections:
                        section_name = section['ObjectName']
                        section_path = section['ObjectPath']
                        type = section_name.split("'")[0]
                        index = section_path.split(".")[1]
                        if type == 'MovieSceneSubSection':
                            section = index_to_element[int(index)]
                            if 'SubSequence' in section['Properties']:
                                subsequence = section['Properties']['SubSequence']
                                if subsequence is not None:
                                    subsequence_name = subsequence['ObjectName']
                                    subsequence_path = subsequence['ObjectPath']
                                    type = subsequence_name.split("'")[0]
                                    true_name = subsequence_name.split("'")[1]
                                    true_path = subsequence_path.split(".")[0]
                                    index = subsequence_path.split(".")[1]
                                    if type == 'LevelSequence':
                                        text += parseCutscene(subsequence_path, true_name, true_path, index, True)
    if 'ObjectBindings' in movie_scene['Properties']:
        bindings = movie_scene['Properties']['ObjectBindings']
        for binding in bindings:
            tracks = binding['Tracks']
            for track in tracks:
                name = track['ObjectName']
                path = track['ObjectPath']
                type = name.split("'")[0]
                index = path.split(".")[1]
                if type == 'BP_SequencerLineTrack_C':
                    track = index_to_element[int(index)]
                    if 'Sections' not in track['Properties']:
                        text += ';(Empty Dialogue Interval)\n' if LOCALE == 'en' else ';(空白间隔)\n'
                    else:
                        lines = track['Properties']['Sections']
                        for line in lines:
                            line_name = line['ObjectName']
                            line_path = line['ObjectPath']
                            type = line_name.split("'")[0]
                            index = line_path.split(".")[1]
                            if type == 'BP_SequencerLineSection_C':
                                line = index_to_element[int(index)]
                                if 'LineId[1]' not in line['Properties']:
                                    text += ';(Empty Dialogue Interval)\n' if LOCALE == 'en' else ';(空白间隔)\n'
                                else:
                                    line_id = line['Properties']['LineId[1]']
                                    speaker = dialogue_line[line_id]['SpeakerTag'] if line_id in dialogue_line else 'None'
                                    line_text = getText('LDLG_Text_ZH_' + line_id, 'None')
                                    sep = "：'''" if LOCALE == 'zh' else ":''' "
                                    try_get_temp_name = dialogue_temp_name.get(line_id + '_TempNTID', {})
                                    if try_get_temp_name:
                                        char_name = getText(try_get_temp_name['l10ntemp_name'], try_get_temp_name['temp_name'])
                                    else:
                                        char_name = character_tag_to_char_map.get(speaker, speaker)
                                    if speaker == 'None' and line_text == 'None':
                                        text += ';(Empty Dialogue Interval)\n' if LOCALE == 'en' else ';(空白间隔)\n'
                                    else:
                                        text += f":'''{char_name}{sep}{line_text}\n"
                elif  type == 'BP_BlackScreenTextTrack_C':
                    track = index_to_element[int(index)]
                    if 'Sections' not in track['Properties']:
                        text += ';(Empty Black Screen)\n' if LOCALE == 'en' else ';(空白黑屏)\n'
                    else:
                        lines = track['Properties']['Sections']
                        text += ';(Start Black Screen)\n' if LOCALE == 'en' else ';(开始黑屏)\n'
                        for line in lines:
                            line_name = line['ObjectName']
                            line_path = line['ObjectPath']
                            type = line_name.split("'")[0]
                            index = line_path.split(".")[1]
                            if type == 'BP_BlackScreenTextSection_C':
                                line = index_to_element[int(index)]
                                if 'TextLineID[1]' not in line['Properties']:
                                    text += ';(Empty Black Screen)\n' if LOCALE == 'en' else ';(空白黑屏)\n'
                                else:
                                    line_id = line['Properties']['TextLineID[1]']
                                    speaker = dialogue_line[line_id]['SpeakerTag'] if line_id in dialogue_line else 'None'
                                    line_text = getText('LDLG_Text_ZH_' + line_id, 'None')
                                    sep = "：'''" if LOCALE == 'zh' else ":''' "
                                    try_get_temp_name = dialogue_temp_name.get(line_id + '_TempNTID', {})
                                    if try_get_temp_name:
                                        char_name = getText(try_get_temp_name['l10ntemp_name'],
                                                            try_get_temp_name['temp_name'])
                                    else:
                                        char_name = character_tag_to_char_map.get(speaker, speaker)
                                    if speaker == 'None' and line_text == 'None':
                                        text += ';(Empty Black Screen)\n' if LOCALE == 'en' else ';(空白黑屏)\n'
                                    else:
                                        text += f":'''{char_name}{sep}{line_text}\n"
                        text += ';(End Black Screen)\n' if LOCALE == 'en' else ';(结束黑屏)\n'

    text += '\n'
    return text


def genSingleCutscene(cutscene_id, _cutscene=None):
    if not _cutscene:
        _cutscene = cutscene[cutscene_id]
    ls = _cutscene['LevelSequence'].split('.')
    text = parseCutscene(cutscene_id, ls[1], ls[0], ls[1])
    replacements = {
        'RedBold': '{{{{Color|Pink|{}}}}}',
        'BlueBold': '{{{{Color|Blue|{}}}}}',
        'Italic': "''{}''",
        'RedBoldItalic': "{{{{Color|Pink|''{}''}}}}",
        'BlueBoldItalic': "{{{{Color|Blue|''{}''}}}}",
    }
    text = replaceTags(text, replacements)
    return text

def generateCutscenes():
    result = ""
    for cutscene_id in cutscene.keys():
        result += genSingleCutscene(cutscene_id)
    return result



type_map = {
    '200': 1,
    '201': 5,
    '202': 3,
    '203': 4,
    '204': 2,
    '205': 6,
    '206': 7,
    '207': 8,
    '208': 8,
    '209': 8,
    '210': 8,
    '211': 8,
    '212': 8,
    '213': 8,
    '214': 8,
    '215': 8,
    '216': 8,
    '217': 8,
    '218': 8,
    '219': 8,
    '220': 8,
}

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
    return getNSLOCTEXT(character_table[str(id)]['name'])

def generateComments(id):
    template_args = {}
    extra = item_extra_table.get(str(id), {})
    if str(extra['npc1']) not in character_table:
        return ''
    template_args['comment_1'] = getText(extra['l10ncomment1'], extra['comment1'])
    template_args['user_1'] = getNPCName(str(extra['npc1']))
    template_args['user_1'] = r'{{subst:ktc}}' if template_args['user_1'] == 'Kilo the Cadenceborn' else template_args['user_1']
    template_args['comment_2'] = getText(extra['l10ncomment2'], extra['comment2'])
    template_args['user_2'] = getNPCName(str(extra['npc2']))
    template_args['user_2'] = r'{{subst:ktc}}' if template_args['user_2'] == 'Kilo the Cadenceborn' else template_args['user_2']
    return generateGeneralMediaWikiTemplate('Comments', template_args)


def genSinglePiece(item_id, _item=None, _actual_item=None):
    if not _item:
        _item = item_extra[item_id]
    if not _actual_item:
        _actual_item = item.get(str(item_id), {})
    result = ''
    if _item['ItemType'] == 1659907149:
        result += 'ID: ' + str(item_id) + '\n'
        result += getText(_actual_item['NameKey'], _actual_item['NameKey']) + '\n'
        result += getText(_actual_item['UseKey'], _actual_item['UseKey']) + '\n'
        result += getText(_actual_item['DescriptionKey'], _actual_item['DescriptionKey']) + '\n'
        result += 'Rarity: ' + str(_actual_item['Rarity']) + '\n'
        result += 'Type: ' + getText(display_type[str(_actual_item['DisplayTypeID'])]['TypeKey'],
                                       display_type[str(_actual_item['DisplayTypeID'])]['TypeKey']) + '\n'
        result += 'Tags: ' + ', '.join(
            [getText(tags[str(i)]['NameKey'], tags[str(i)]['NameKey']) for i in _item['Tag']]) + '\n'
        type_id = _actual_item['DisplayTypeID']
        if type_id >= 200 and type_id <= 220:
            attribute_id = _actual_item['AttributeID']
            factor = factors[str(attribute_id)]['Value'] / 100
            rank = []
            for v in _item['Stats']:
                for k, r in ranks.items():
                    if v / factor >= int(r['Min']) and v / factor < int(r['Max']):
                        rank.append(r['Text'])
            result += 'Ranks: ' + ', '.join(rank) + '\n'
            result += 'BaseStats: ' + ', '.join([str(i) for i in _item['Stats']]) + '\n'
            if not SIMPLE:
                type = type_map[str(type_id)]
                result += 'StatTable: \n'
                this_level = level[str(type)][str(_actual_item['Rarity'])]
                material_text = ''
                for condition in this_level['Condition']:
                    result += 'Level' + str(condition['CurrentLevel']) + ': ' + ', '.join(
                        [str(ceil(i * condition['BaseIncrementStats'] / 100 + i)) for i in _item['Stats']]) + \
                              material_text + (', Condition: ' + getText(condition['ConditionKey'],
                                                                           condition['ConditionKey']) if getText(
                        condition['ConditionKey'], '') else '') + '\n'
                    material_text = ', Materials: ' + ', '.join(
                        [getText(item[str(i[0])]['NameKey'], item[str(i[0])]['NameKey']) + ' x' + str(i[1]) for i in
                         condition.get('Material', [])])
                this_renew = renew[str(type)][str(_actual_item['Rarity'])]
                highest_value = _item['Stats'][0]
                highest = 0
                for i in range(1, len(_item['Stats'])):
                    if _item['Stats'][i] > highest_value:
                        highest_value = _item['Stats'][i]
                        highest = i
                result += 'Renew: ' + ', '.join(
                    [str(ceil(i * this_renew['BaseIncrementStats'] / 100 + i)) for i in _item['Stats']]) + \
                          ', Materials: ' + ', '.join(
                    [getText(item[str(i[0])]['NameKey'], item[str(i[0])]['NameKey']) + ' x' + str(i[1]) for i in
                     this_renew['NormalMaterial']]) + \
                          ', ' + getText(item[str(this_renew['SpecialMaterial'][highest][0])]['NameKey'],
                                           item[str(this_renew['SpecialMaterial'][highest][0])]['NameKey']) + ' x' + str(
                    this_renew['SpecialMaterial'][highest][1]) + '\n'
        if not SIMPLE:
            result += 'Comments: \n'
            result += joinCharacter(_item['Comment1NPC']) + ': ' + getText(_item['Comment1Key'],
                                                                                _item['Comment1Key']) + '\n'
            result += joinCharacter(_item['Comment2NPC']) + ': ' + getText(_item['Comment2Key'],
                                                                                _item['Comment2Key']) + '\n'
        result += 'Obtains: \n'
        for obtain in _item['ObtainMethod']:
            result += getText(obtains[str(obtain)]['DescriptionKey'], obtains[str(obtain)]['DescriptionKey']) + '\n'
        result += 'IconTexture1: ' + _actual_item['Texture1'] + '\n'
        result += 'IconTexture2: ' + _actual_item['Texture2'] + '\n'
        result += 'ShowpicTexture: ' + _item['ShowpicTexture'] + '\n'
        result += 'WikiTemplates: \n'
        if item_table[str(item_id)]['minor_type'] != 413:
            result += generateScore(item_id) + '\n'
        result += generateComments(item_id) + '\n'
        result += '\n'
    elif _item['ItemType'] == -1078125975:
        result += 'ID: ' + str(item_id) + '\n'
        if _actual_item:
            result += getText(_actual_item['NameKey'], _actual_item['NameKey']) + '\n'
            result += getText(_actual_item['UseKey'], _actual_item['UseKey']) + '\n'
            result += getText(_actual_item['DescriptionKey'], _actual_item['DescriptionKey']) + '\n'
            result += 'Rarity: ' + str(_actual_item['Rarity']) + '\n'
        if len(_item['ShowpicTexture']) > 0:
            result += 'ShowpicTexture: ' + _item['ShowpicTexture'][0] + '\n'
        result += '\n'
    return result


def generatePieces():
    result = ""
    for item_id in item_extra:
        result += genSinglePiece(item_id)
    return result


def genSingleSuit(suit_id, _suit=None):
    if not _suit:
        _suit = suit[suit_id]
    result = 'ID: ' + str(suit_id) + '\n'
    result += getText(_suit['NameKey'], _suit['NameKey']) + '\n'
    result += getText(_suit['DescriptionKey'], _suit['DescriptionKey']) + '\n'
    result += 'Rarity: ' + str(_suit['Rarity']) + '\n'
    result += 'Comments: \n'
    result += joinCharacter(_suit['Comment1NPC']) + ': ' + getText(_suit['Comment1Key'], _suit['Comment1Key']) + '\n'
    result += joinCharacter(_suit['Comment2NPC']) + ': ' + getText(_suit['Comment2Key'], _suit['Comment2Key']) + '\n'
    result += 'Obtains: \n'
    for obtain in _suit['ObtainMethod']:
        result += getText(obtains[str(obtain)]['DescriptionKey'], obtains[str(obtain)]['DescriptionKey']) + '\n'
    result += 'Pieces: \n'
    for piece in _suit['Parts']:
        if str(piece) not in item:
            result += f'Item_{piece}\n'
            continue
        actual_item = item[str(piece)]
        result += getText(actual_item['NameKey'], actual_item['NameKey']) + '\n'
    result += 'CollectionReward: ' + str(_suit['CollectionReward']) + '\n'
    result += 'ShowpicTexture1: ' + _suit['Texture1'] + '\n'
    result += 'ShowpicTexture2: ' + _suit['Texture2'] + '\n'
    result += 'ShowpicTexture3: ' + _suit['Texture3'] + '\n'
    result += '\n'
    return result

def generateSuits():
    result = ""
    for suit_id in suit:
        result += genSingleSuit(suit_id)
    return result


def genSingleItem(item_id, _item=None):
    if not _item:
        _item = item[item_id]
    result = 'ID: ' + str(item_id) + '\n'
    result += getText(_item['NameKey'], _item['NameKey']) + '\n'
    result += getText(_item['UseKey'], _item['UseKey']) + '\n'
    result += getText(_item['DescriptionKey'], _item['DescriptionKey']) + '\n'
    result += 'Rarity: ' + str(_item['Rarity']) + '\n'
    if str(_item['DisplayTypeID']) in display_type:
        result += 'Type: ' + getText(display_type[str(_item['DisplayTypeID'])]['TypeKey'],
                                       display_type[str(_item['DisplayTypeID'])]['TypeKey']) + '\n'
    if 'GalleryScore' in _item:
        result += 'GalleryScore: ' + str(_item['GalleryScore']) + '\n'
    if item_id in formulas:
        result += 'Formula: ' + ', '.join(
            [getText(item[str(i[0])]['NameKey'], item[str(i[0])]['NameKey']) + ' x' + str(i[1]) for i in
             formulas[item_id]['Material']]) + '\n'
        result += 'Output: ' + getText(item[str(formulas[item_id]['ItemID'])]['NameKey'],
                                         item[str(formulas[item_id]['ItemID'])]['NameKey']) + '\n'
    result += 'IconTexture1: ' + _item['Texture1'] + '\n'
    result += 'IconTexture2: ' + _item['Texture2'] + '\n'
    result += '\n'
    return result


def generateItems():
    result = ""
    for singleItem in item:
        result += genSingleItem(singleItem)
    return result

def genSingleMagicBall(ball_id, _ball=None):
    if not _ball:
        _ball = magic_ball[ball_id]
    result = 'ID: ' + str(ball_id) + '\n'
    result += getText(item[str(ball_id)]['NameKey'], item[str(ball_id)]['NameKey']) + '\n'
    result += getText(item[str(ball_id)]['UseKey'], item[str(ball_id)]['UseKey']) + '\n'
    result += getText(item[str(ball_id)]['DescriptionKey'], item[str(ball_id)]['DescriptionKey']) + '\n'
    result += 'Rarity: ' + str(item[str(ball_id)]['Rarity']) + '\n'
    attribute_id = 1301
    factor = factors[str(attribute_id)]['Value'] / 100
    rank = []
    for v in _ball['Stats']:
        for k, r in ranks.items():
            if v / factor >= int(r['Min']) and v / factor < int(r['Max']):
                rank.append(r['Text'])
    result += 'Ranks: ' + ', '.join(rank) + '\n'
    result += 'Tag: ' + (getText(tags[str(_ball['Tag'])]['NameKey'], tags[str(_ball['Tag'])]['NameKey']) if str(_ball['Tag']) in tags else "TagID_" + str(_ball['Tag'])) + '\n'
    result += 'Stats: ' + ', '.join([str(i) for i in _ball['Stats']]) + '\n'
    result += 'StatTable: \n'
    result += 'Level0: ' + ', '.join([str(i) for i in _ball['Stats']]) + '\n'
    this_level = magic_ball_level[str(item[str(ball_id)]['Rarity'])]
    for lvl in this_level:
        level = this_level[lvl]
        result += 'Level' + str(level['CurrentLevel']) + ': ' + ', '.join(
            [str(ceil(i * level['BaseIncrementStats'] / 10000 + i)) for i in _ball['Stats']]) + \
                  ', EXP: ' + str(level['Exp']) + '\n'
    result += 'IconTexture1: ' + item[str(ball_id)]['Texture1'] + '\n'
    result += 'IconTexture2: ' + item[str(ball_id)]['Texture2'] + '\n'
    result += '\n'
    return result

def generateMagicBalls():
    result = ""
    for ball_id in magic_ball:
        result += genSingleMagicBall(ball_id)
    return result







def buildLuaReturn(data: dict):
    def formatValue(value):
        if isinstance(value, str):
            return f"'{value.replace('\'', r'\'')}'"
        elif isinstance(value, int):
            return f"{value}"
        elif isinstance(value, list):
            return f"{{{', '.join([formatValue(i) for i in value])}}}"
        elif isinstance(value, dict):
            return f"{{{', '.join([f'{k} = {formatValue(v)}' for k, v in value.items()])}}}"
        else:
            return

    for id in list(data.keys()):
        for key in list(data[id].keys()):
            if key.startswith('_'):
                del data[id][key]
    result = 'return {\n'
    for k, v in data.items():
        key = k.replace("'", r"\'").strip()
        result += f"    ['{key}'] = {formatValue(v)},\n"
    result += '}\n'
    return result

if LOCALE == 'zh':
    wiki_style_map = [
        '典雅',
        '清新',
        '甜美',
        '性感',
        '帅气',
    ]
else:
    wiki_style_map = [
        'Elegant',
        'Fresh',
        'Sweet',
        'Sexy',
        'Cool',
    ]

wiki_type_map = {
    200: 'Hair',
    201: 'Dresses',
    202: 'Tops',
    203: 'Bottoms',
    204: 'Outerwear',
    205: 'Socks',
    206: 'Shoes',
    207: 'Hair Accessories',
    208: 'Headwear',
    209: 'Earrings',
    210: 'Neckwear',
    211: 'Bracelets',
    212: 'Chokers',
    213: 'Gloves',
    214: 'Handhelds',
    215: 'Face Decorations',
    216: 'Chest Accessories',
    217: 'Pendants',
    218: 'Backpieces',
    219: 'Rings',
    220: 'Special',
    221: 'Full Makeup',
    222: 'Base Makeup',
    223: 'Eyebrows',
    224: 'Eyelashes',
    225: 'Contact Lenses',
    226: 'Lips',
    227: 'Skin Tones',
    228: 'Arm Decorations',
    413: 'Ability Handhelds',
    1300: 'Eurekas',
    1301: 'Eurekas',
    1302: 'Eurekas',
}

def generateWikiClothesDict(is_id: bool = False):
    result = {}
    for id in item:
        if item[id]['CategoryID'] == 2 and id in item_extra:
            _item = item_extra[id]
            style = wiki_style_map[_item['Major']]
            key = id if is_id else (getText(item[id]['NameKey'], item[id]['NameKey']) if LOCALE == 'en' else getText(item[id]['NameKey'], item[id]['NameText']))
            result[key] = {
                'style': style,
                'category': wiki_type_map[item[id]['DisplayTypeID']] if LOCALE == 'en' else display_type[str(item[id]['DisplayTypeID'])]['TypeName'],
                'rarity': str(item[id]['Rarity']),
                'stats': _item['Stats'],
            }
            if LOCALE == 'zh':
                result[key]['icon'] = getEnText(item[id]['NameKey'], item[id]['NameKey'])
    return result

def generateWikiSuitsDict(is_id: bool = False):
    result = {}
    for id in suit:
        _suit = suit[id]
        sample_item = item_extra[str(_suit['Parts'][0])]
        highest_value = sample_item['Stats'][0]
        highest = 0
        for i in range(1, len(sample_item['Stats'])):
            if sample_item['Stats'][i] > highest_value:
                highest_value = sample_item['Stats'][i]
                highest = i
        style = wiki_style_map[highest]
        key = id if is_id else getText(_suit['NameKey'], _suit['NameKey'])
        result[key] = {
            'style': style,
            'category': 'Outfits' if LOCALE == 'en' else '套装',
            'rarity': str(_suit['Rarity']),
        }
        if LOCALE == 'zh':
            result[key]['icon'] = getEnText(_suit['NameKey'], _suit['NameKey'])
    return result

if LOCALE == 'zh':
    major_type_map = {
        1: '货币',
        2: '服装',
        4: '消耗品',
        7: '头像框',
        9: '拍照道具',
        11: '设计图',
        16: '大喵斗篷',
    }
else:
    major_type_map = {
        2: 'Clothes',
        4: 'Consumable',
        7: 'Avatar Frame',
        9: 'Photo Prop',
        11: 'Sketch',
        16: 'Momo\'s Cloaks',
    }

def generateWikiItemsDict(is_id: bool = False):
    result = {}
    for id in item:
        _item = item[id]
        key = id if is_id else (getText(_item['NameKey'], _item['NameKey']) if LOCALE == 'en' else getText(_item['NameKey'], _item['NameText']))
        if str(_item['DisplayTypeID']) in display_type:
            category = wiki_type_map.get(_item['DisplayTypeID'], getText(display_type[str(
                _item['DisplayTypeID'])]['TypeKey'], display_type[str(_item['DisplayTypeID'])]['TypeKey'])) if LOCALE == 'en' else display_type[str(_item['DisplayTypeID'])]['TypeName']
        else:
            category = 'Unknown' if LOCALE == 'en' else '无'
        if key in result:
            if _item['CategoryID'] == 2 or _item['CategoryID'] == 1 or _item['CategoryID'] == 16:
                new_old_key = (key + f' ({major_type_map[result[key]["_MajorType"]]})') if LOCALE == 'en' else (key + f'（{major_type_map[result[key]["_MajorType"]]}）')
                result[new_old_key] = result.pop(key)
            elif _item['CategoryID'] != result[key]["_MajorType"]:
                key = (key + f' ({major_type_map[_item["CategoryID"]]})') if LOCALE == 'en' else (key + f'（{major_type_map[_item["CategoryID"]]}）')
        result[key] = {
            'category': category,
            'rarity': str(_item['Rarity']),
            '_MajorType': _item['CategoryID'],
        }
        if LOCALE == 'zh':
            result[key]['icon'] = getEnText(_item['NameKey'], _item['NameKey'])
    return result

if LOCALE == 'zh':
    magic_ball_type_map = [
        '无',
        '祝福闪光·头部',
        '祝福闪光·手部',
        '祝福闪光·脚部',
    ]
else:
    magic_ball_type_map = [
        'None',
        'Eureka: Head',
        'Eureka: Hands',
        'Eureka: Feet',
    ]

def generateWikiMagicBallsDict(is_id: bool = False):
    result = {}
    for id in magic_ball:
        _ball = magic_ball[id]
        _item = item[id]
        highest_value = _ball['Stats'][0]
        highest = 0
        for i in range(1, len(_ball['Stats'])):
            if _ball['Stats'][i] > highest_value:
                highest_value = _ball['Stats'][i]
                highest = i
        style = wiki_style_map[highest]
        key = id if is_id else getText(_item['NameKey'], _item['NameKey'])
        result[key] = {
            'style': style,
            'category': magic_ball_type_map[_ball['Type']],
            'rarity': str(_item['Rarity']),
            'stats': _ball['Stats'],
        }
        if LOCALE == 'zh':
            result[key]['icon'] = getEnText(_item['NameKey'], _item['NameKey'])
    return result

def generateWikiMomosCloaksDict(is_id: bool = False):
    result = {}
    for id in item:
        if item[id]['CategoryID'] == 16:
            _item = item_extra[id]
            key = id if is_id else getText(item[id]['NameKey'], item[id]['NameKey'])
            result[key] = {
                'category': 'Momo\'s Cloak' if LOCALE == 'en' else '大喵斗篷',
                'rarity': str(item[id]['Rarity']),
            }
            if LOCALE == 'zh':
                result[key]['icon'] = getEnText(item[id]['NameKey'], item[id]['NameKey'])
    return result


def post():
    loadConfigs()

    buildCharacterTagToCharMap()
    buildNextDlgStageToChoiceMap()
    buildDialogueUidToNodeMap()
    buildDlgStageToCharMap()
    buildMissionTagToNameMap()
    buildCutsceneUidToNodeMap()

    with open('cfg/pieces.txt', 'w', encoding='utf-8') as f:
        f.write(generatePieces())

    with open('cfg/suits.txt', 'w', encoding='utf-8') as f:
        f.write(generateSuits())

    with open('cfg/items.txt', 'w', encoding='utf-8') as f:
        f.write(generateItems())

    with open('cfg/magic_balls.txt', 'w', encoding='utf-8') as f:
        f.write(generateMagicBalls())

    with open('cfg/dialogues.txt', 'w', encoding='utf-8') as f:
        f.write(generateDialogues())

    with open('cfg/cutscenes.txt', 'w', encoding='utf-8') as f:
        f.write(generateCutscenes())

    with open('cfg/pieces.lua', 'w', encoding='utf-8') as f:
        f.write(buildLuaReturn(generateWikiClothesDict()))

    with open('cfg/suits.lua', 'w', encoding='utf-8') as f:
        f.write(buildLuaReturn(generateWikiSuitsDict()))

    with open('cfg/items.lua', 'w', encoding='utf-8') as f:
        f.write(buildLuaReturn(generateWikiItemsDict()))

    with open('cfg/magic_balls.lua', 'w', encoding='utf-8') as f:
        f.write(buildLuaReturn(generateWikiMagicBallsDict()))

    with open('cfg/momos_cloaks.lua', 'w', encoding='utf-8') as f:
        f.write(buildLuaReturn(generateWikiMomosCloaksDict()))