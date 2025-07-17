import json
import os.path

import xmltodict
import subprocess
import shutil


bank_dict = {}

def fnv_hash_32(data: str):
    hash_num = 2166136261
    data = data.lower().encode()
    for i in data:
        hash_num = ((hash_num * 16777619) & 0xffffffff) ^ i
    return hash_num

def generate_bank_data(I_N_CORE_DATA_PATH):
    result = subprocess.run(['python', os.path.abspath('./wwiser.pyz'), '-d', 'xml', '-dn', os.path.abspath('./cfg/banks'), '*.bnk', '-r'],
                            capture_output=True, text=True, shell=True, cwd=f'{I_N_CORE_DATA_PATH}/X6Game/Content/Audio')
    print(result.stdout)

def load_bank_xml():
    global bank_dict
    if os.path.exists("cfg/banks_temp.json"):
        with open("cfg/banks_temp.json", 'r') as f:
            bank_dict_old = json.load(f)
            print("[Main] Bank data loaded from cache. If you want to reload, delete the `banks_temp.json` file.")
            bank_dict = bank_dict_old
            return
    with open("cfg/banks.xml", 'r', encoding='utf-8') as f:
        xml_string = f.read()
    data_dict = xmltodict.parse("<base>" + xml_string + "</base>")
    hash_map = {}
    for i in ["SFX", "Chinese(PRC)", "English(US)", "Japanese"]:
        hash_map[str(fnv_hash_32(i))] = i
    for bank in data_dict["base"]["root"]:
        bank_cont = parseXmlNode(bank)
        lang = bank_cont["BankHeader"]["AkBankHeader"]["dwLanguageID"]["@value"]
        if hash_map[lang] not in bank_dict:
            bank_dict[hash_map[lang]] = {}
        bank_dict[hash_map[lang]][bank["@filename"]] = bank_cont

    with open("cfg/banks_temp.json", 'w') as f:
        json.dump(bank_dict, f, indent=4)

def parseXmlNode(node):
    result = node
    parseXmlObj("field", node, result)
    parseXmlObj("object", node, result)
    parseXmlLst(node, result)
    return result

def parseXmlObj(obj_name, obj, result):
    if obj_name in obj:
        if isinstance(obj[obj_name], list):
            for item in obj[obj_name]:
                if item["@name"] not in result:
                    result[item["@name"]] = parseXmlNode(item)
                else:
                    if not isinstance(result[item["@name"]], list):
                        foo = result[item["@name"]]
                        result[item["@name"]] = []
                        result[item["@name"]].append(foo)
                    result[item["@name"]].append(parseXmlNode(item))
        elif isinstance(obj[obj_name], dict):
            result[obj[obj_name]["@name"]] = parseXmlNode(obj[obj_name])
        del result[obj_name]

def parseXmlLst(lst, result):
    if "list" in lst:
        lst = lst["list"]
        if isinstance(lst, list):
            for item in lst:
                result[item["@name"]] = []
                appendXmlLstElement("field", item, result[item["@name"]])
                appendXmlLstElement("object", item, result[item["@name"]])
                appendXmlLstElement("list", item, result[item["@name"]])
        else:
            result[lst["@name"]] = []
            appendXmlLstElement("field", lst, result[lst["@name"]])
            appendXmlLstElement("object", lst, result[lst["@name"]])
            appendXmlLstElement("list", lst, result[lst["@name"]])
        del result["list"]

def appendXmlLstElement(obj_name, obj, lst):
    if obj_name in obj:
        if isinstance(obj[obj_name], list):
            for item in obj[obj_name]:
                lst.append(parseXmlNode(item))
        elif isinstance(obj[obj_name], dict):
            lst.append(parseXmlNode(obj[obj_name]))
        del obj[obj_name]

skip_num = 0
completed_files = []

def elegantRename(hash_path, voice_path, ext="wem", log_area="External"):
    old_file_name = f"{hash_path}.{ext}"
    new_file_name = f"{voice_path}.{ext}"
    if os.path.exists(new_file_name):
        os.remove(new_file_name)
    global completed_files
    if os.path.exists(old_file_name):
        shutil.copy2(old_file_name, new_file_name)
        if old_file_name not in completed_files:
            completed_files.append(old_file_name)
    else:
        print(f"[{log_area}] {old_file_name} -> {new_file_name} not found!")
        global skip_num
        skip_num += 1

def resort_event_wems(I_N_CORE_DATA_PATH, I_N_STRM_DATA_PATH):
    def getLoadedItems(bank):
        hirc = bank.get("HircChunk", {})
        loaded_items = hirc.get("listLoadedItem", [])
        loaded_items_map = {}
        for item in loaded_items:
            loaded_items_map[item.get("ulID", item.get("ulStateID", ""))["@value"]] = item
        return loaded_items_map

    def findAudioNode(nodes, audioNodeIdToName, path = ""):
        for node in nodes:
            if "audioNodeId" in node:
                audioNodeIdToName[node["audioNodeId"]["@value"]] = path + node["key"].get("@hashname", node["key"]["@value"])
            elif "pNodes" in node:
                findAudioNode(node["pNodes"], audioNodeIdToName, path + node["key"].get("@hashname", node["key"]["@value"]) + "/")

    def findSwitchNode(nodes, switchNodeIdToName):
        for node in nodes:
            if int(node["ulNumItems"]["@value"]) > 0:
                if int(node["ulNumItems"]["@value"]) == 1:
                    switchNodeIdToName[node["NodeList"]["NodeID"]["@value"]] = node["ulSwitchID"].get("@hashname",
                                                                                                    node["ulSwitchID"][
                                                                                                        "@value"])
                else:
                    for item in node["NodeList"]["NodeID"]:
                        switchNodeIdToName[item["@value"]] = node["ulSwitchID"].get("@hashname",
                                                                                   node["ulSwitchID"]["@value"])

    def getChilds(node, result):
        if "ulNumChilds" in node:
            if int(node["ulNumChilds"]["@value"]) > 0:
                if int(node["ulNumChilds"]["@value"]) == 1:
                    result.append(node["ulChildID"]["@value"])
                else:
                    for child in node["ulChildID"]:
                        result.append(child["@value"])
        return result

    def findMusicSound(sound_id, musicSegments, musicTracks, musicRanSeqCntrs, musicSwitchCntrs, path, result):
        if sound_id in musicSwitchCntrs:
            for child in musicSwitchCntrs[sound_id]:
                subpath = path
                subpath += f"/{musicSwitchCntrs[sound_id][child]}"
                findMusicSound(child, musicSegments, musicTracks, musicRanSeqCntrs, musicSwitchCntrs, subpath, result)
        if sound_id in musicRanSeqCntrs:
            childs = []
            getChilds(musicRanSeqCntrs[sound_id], childs)
            for child in childs:
                findMusicSound(child, musicSegments, musicTracks, musicRanSeqCntrs, musicSwitchCntrs, path, result)
        if sound_id in musicSegments:
            childs = []
            getChilds(musicSegments[sound_id], childs)
            for child in childs:
                findMusicSound(child, musicSegments, musicTracks, musicRanSeqCntrs, musicSwitchCntrs, path, result)
        if sound_id in musicTracks:
            for source in musicTracks[sound_id]:
                subpath = path
                subpath += f"/{source["AkMediaInformation"]["sourceID"]["@value"]}"
                result[source["AkMediaInformation"]["sourceID"]["@value"]] = subpath

    event_name_to_path = {}
    for root, dirs, files in os.walk(f"{I_N_STRM_DATA_PATH}/X6Game/Content/Audio/Events"):
        for file in files:
            if file.endswith(".json") or file.endswith(".uasset"):
                event_name = file.replace(".json", "").replace(".uasset", "")
                path = root.replace(I_N_STRM_DATA_PATH, "").replace("\\", "/").replace("/X6Game/Content/Audio/Events", "")
                event_name_to_path[event_name] = path

    def findSound(sound_id, loaded_items, bnk_name, lang, path, results):
        def renameSource(source, index, source_index):
            if source["AkMediaInformation"]["sourceID"]["@value"] != "0":
                source_sound_path = f"{I_N_CORE_DATA_PATH}/X6Game/Content/Audio/Media/{lang}"
                language_specific = source["AkMediaInformation"]["uSourceBits"]["bIsLanguageSpecific"]["@value"]
                if language_specific == "0":
                    source_sound_path = f"{I_N_CORE_DATA_PATH}/X6Game/Content/Audio/Media"
                name = os.path.basename(source["AkMediaInformation"]["sourceID"]["@guidname"]).replace(".wav", "") if "@guidname" in source["AkMediaInformation"]["sourceID"] else source["AkMediaInformation"]["sourceID"]["@value"]
                file2rename = f"{source_sound_path}/{source["AkMediaInformation"]["sourceID"]["@value"]}"
                if bnk_name in event_name_to_path:
                    file_destination = f"cfg/sound{event_name_to_path[bnk_name]}/{path}/{index}{'~' if source_index else ''}{source_index}~{name}{'~' + lang if language_specific != "0" else ''}"
                    if not os.path.exists(f"cfg/sound{event_name_to_path[bnk_name]}/{path}"):
                        os.makedirs(f"cfg/sound{event_name_to_path[bnk_name]}/{path}")
                else:
                    file_destination = f"cfg/sound/UnknownPaths/{bnk_name}/{path}/{index}{'~' if source_index else ''}{source_index}~{name}{'~' + lang if language_specific != "0" else ''}"
                    if not os.path.exists(f"cfg/sound/UnknownPaths/{bnk_name}/{path}"):
                        os.makedirs(f"cfg/sound/UnknownPaths/{bnk_name}/{path}")
                results.append((file2rename, file_destination))

        if sound_id in loaded_items:
            name = loaded_items[sound_id]["@name"]

            if name == "CAkSwitchCntr":
                node_id2name = {}
                findSwitchNode(loaded_items[sound_id]["SwitchCntrInitialValues"]["SwitchList"], node_id2name)
                for child in node_id2name:
                    subpath = path
                    subpath += f"/{node_id2name[child]}"
                    findSound(child, loaded_items, bnk_name, lang, subpath, results)

            if name == "CAkRanSeqCntr":
                childs = []
                getChilds(loaded_items[sound_id]["RanSeqCntrInitialValues"]["Children"], childs)
                for child in childs:
                    findSound(child, loaded_items, bnk_name, lang, path, results)

            if name == "CAkLayerCntr":
                childs = []
                getChilds(loaded_items[sound_id]["LayerCntrInitialValues"]["Children"], childs)
                for child in childs:
                    findSound(child, loaded_items, bnk_name, lang, path, results)

            if name == "CAkSound":
                source = loaded_items[sound_id]["SoundInitialValues"]["AkBankSourceData"]
                renameSource(source, loaded_items[sound_id]["@index"], "")

            if name == "CAkMusicSwitchCntr":
                node_id2name = {}
                findAudioNode(loaded_items[sound_id]["MusicSwitchCntrInitialValues"]["AkDecisionTree"]["pNodes"],
                              node_id2name)
                for child in node_id2name:
                    subpath = path
                    subpath += f"/{node_id2name[child]}"
                    findSound(child, loaded_items, bnk_name, lang, subpath, results)

            if name == "CAkMusicRanSeqCntr":
                childs = []
                getChilds(
                    loaded_items[sound_id]["MusicRanSeqCntrInitialValues"]["MusicTransNodeParams"]["MusicNodeParams"][
                        "Children"], childs)
                for child in childs:
                    findSound(child, loaded_items, bnk_name, lang, path, results)

            if name == "CAkMusicSegment":
                childs = []
                getChilds(loaded_items[sound_id]["MusicSegmentInitialValues"]["MusicNodeParams"]["Children"], childs)
                for child in childs:
                    findSound(child, loaded_items, bnk_name, lang, path, results)

            if name == "CAkMusicTrack":
                for source in loaded_items[sound_id]["MusicTrackInitialValues"]["pSource"]:
                    renameSource(source, loaded_items[sound_id]["@index"], source["@index"])

    if not os.path.exists(f"cfg/sound"):
        os.makedirs(f"cfg/sound")

    for lang in bank_dict:
        for bank_name in bank_dict[lang]:
            print(f"[Event] {lang}: {bank_name}")
            bank = bank_dict[lang][bank_name]

            loaded_items_map = getLoadedItems(bank)

            processed = False
            global completed_files

            for item_id in loaded_items_map:
                item = loaded_items_map[item_id]
                if item["@name"] == "CAkEvent":
                    event_id = item["ulID"]["@value"]
                    event_name = item["ulID"].get("@hashname", event_id)
                    for action in item["EventInitialValues"]["actions"]:
                        action_item = loaded_items_map[action["ulActionID"]["@value"]]
                        if action_item["@name"] == "CAkActionPlay":
                            params = action_item["ActionInitialValues"]["PlayActionParams"]
                            id_ext = action_item["ActionInitialValues"]["idExt"]["@value"]
                            for sound_lang in (["SFX", lang] if lang != "SFX" else ["SFX", "Chinese(PRC)", "English(US)", "Japanese"]):
                                if sound_lang in bank_dict and params["bankID"]["@hashname"] + ".bnk" in bank_dict[sound_lang]:
                                    sound_bank = bank_dict[sound_lang][params["bankID"]["@hashname"] + ".bnk"]
                                    sound_bank_loaded_items_map = getLoadedItems(sound_bank)

                                    sound_processed = False

                                    normal_sound_path = sound_bank["@path"].replace("\\", "/").replace("./", "")

                                    if id_ext in sound_bank_loaded_items_map:
                                        rename_list = []
                                        findSound(id_ext, sound_bank_loaded_items_map, event_name, lang, event_name, rename_list)
                                        for pair in rename_list:
                                            elegantRename(pair[0], pair[1], "wem", "Event")
                                            pass
                                        sound_processed = True

                                    if sound_processed and f"{normal_sound_path}/{sound_bank["@filename"]}" not in completed_files:
                                        completed_files.append(f"{normal_sound_path}/{sound_bank["@filename"]}")

                    processed = True

            normal_path = bank["@path"].replace("\\", "/").replace("./", "")
            if processed and f"{normal_path}/{bank["@filename"]}" not in completed_files:
                completed_files.append(f"{normal_path}/{bank["@filename"]}")

    global skip_num
    print(f"[Event] skipped {skip_num} files because of unfound hash.")
    skip_num = 0

