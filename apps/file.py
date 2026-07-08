# coding:utf-8

# file.py
import os, zipfile

from config import *

PATH = os.path.join(os.path.expandvars(r"%AppData%"), RECENT_PROJECT_PATH)
os.makedirs(PATH, exist_ok=True)

# 打开一个 zip 文件
def unload():
    for f in os.listdir(PATH):
        file_path = os.path.join(PATH, f)
        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
            except OSError:
                pass

def load(file):
    unload()
    with zipfile.ZipFile(file, "r") as z:
        z.extractall(PATH)