# coding:utf-8

# file.py
import os, zipfile, json

from core.config import *

CACHE_PATH = os.path.join(os.path.expandvars(r"%AppData%"), RECENT_PROJECT_PATH)
os.makedirs(CACHE_PATH, exist_ok=True)

def resolve_app_path(path):
    return os.path.join(CACHE_PATH, path)

# 打开一个项目文件
class Project:
    def __init__(self, file:str):
        if file.endswith((".jenny", ".jen", ".zip")):
            with zipfile.ZipFile(file, "r") as z:
                z.extractall(CACHE_PATH)

# 打开一个 json 文件
def open_json(file):
    with open(resolve_app_path(file), "r", encoding="utf-8") as f:
        content = json.load(f)
    return content

# 读取项目文件
def read():
    index = open_json("index.json")
    song = resolve_app_path(index["song"])
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