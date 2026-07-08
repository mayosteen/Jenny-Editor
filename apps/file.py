# coding:utf-8

# file.py
import os, zipfile, json

from apps.config import *

CACHE_PATH = os.path.join(os.path.expandvars(r"%AppData%"), RECENT_PROJECT_PATH)
os.makedirs(CACHE_PATH, exist_ok=True)

# 打开一个 json 文件
def open_json(file):
    with open(os.path.join(CACHE_PATH, file), "r", encoding="utf-8") as f:
        content = json.load(f)
    return content

# 读取项目文件
def read():
    index = open_json("index.json")
    song = open_json(index["song"])
    chord = open_json(index["chord"])
    return index, song, chord

# 卸载缓存内的文件
def unload():
    for f in os.listdir(CACHE_PATH):
        file_path = os.path.join(CACHE_PATH, f)
        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
            except OSError:
                pass

# 打开一个 zip 文件
def load(file=None):
    if file is not None:
        unload()
        with zipfile.ZipFile(file, "r") as z:
            z.extractall(CACHE_PATH)
    return read()