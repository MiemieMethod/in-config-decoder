import shlex
import shutil
import os
import json
import csv
import subprocess

def uploadImages():
    base_path = r'E:\perfect\src\wikitext\pieces\images'
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith("Icon.png"):
                path = root.replace("\\", "/") + "/" + file
                absolute_path = os.path.abspath(path)
                filename = os.path.basename(file)
                subprocess.run(
                    ['python', 'pwb.py', 'upload', absolute_path, f'-filename:{filename.replace(" ", "_").replace('&', "%26")}',
                     '-summary:Bot：上传图片', r'-descfile:E:\perfect\src\wikitext\pieces\images\icon_desc',
                     '-abortonwarn', '-always'], shell=True, encoding='utf-8',
                    cwd=r"E:\nikki-wiki-bot\core_stable")
            if file.endswith("Showpic.png"):
                path = root.replace("\\", "/") + "/" + file
                absolute_path = os.path.abspath(path)
                filename = os.path.basename(file)
                subprocess.run(
                    ['python', 'pwb.py', 'upload', absolute_path, f'-filename:{filename.replace(" ", "_").replace('&', "%26")}',
                     '-summary:Bot：上传图片', r'-descfile:E:\perfect\src\wikitext\pieces\images\showpic_desc',
                     '-abortonwarn', '-always'], shell=True, encoding='utf-8',
                    cwd=r"E:\nikki-wiki-bot\core_stable")


uploadImages()