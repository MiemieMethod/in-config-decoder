import os
import subprocess

def upload(folder, name):
    subprocess.run(['python', 'pwb.py', 'login'], shell=True, cwd=r"E:\nikki-wiki-bot\core_stable")
    for root, dirs, files in os.walk("E:\\perfect\\src\\wikitext\\" + f"{folder}"):
        for file in files:
            path = root.replace("\\", "/") + "/" + file
            absolute_path = os.path.abspath(path)
            filename = os.path.basename(file).replace(".wikitext", "")
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            subprocess.run(
                ['python', 'pwb.py', 'add_text', f'-page:{filename}', f'-summary:"Bot：创建{name}页面：{filename}',
                 f'-textfile:{absolute_path}', '-create', '-createonly', '-always'], shell=True,
                cwd=r"E:\nikki-wiki-bot\core_stable")



