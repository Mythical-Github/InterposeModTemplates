import os
import sys
import json
import time
import shutil
import psutil
import win32gui
import subprocess
from pathlib import Path

subprocess.run("C:/Users/Mythical/Documents/GitHub/Interpose/modding_workspace/scripts/batch/engine_cook.bat")

old = "C:/Users/Mythical/Documents/GitHub/Interpose/modding_workspace/scripts/python/python_unrealpak/Z_ModLoader_P/KevinSpel/Content/Mods"
new = "C:/Users/Mythical/Downloads/Output/WindowsNoEditor/KevinSpel/Content/Mods"

game_exe = "C:/Program Files (x86)/Steam/steamapps/common/Zedfest/KevinSpel/Binaries/Win64/Zedfest.exe"

if os.path.isdir(old):
    shutil.rmtree(old)
if os.path.isdir(new):
    shutil.copytree(new, old)

subprocess.run("C:/Users/Mythical/Documents/GitHub/Interpose/modding_workspace/scripts/python/python_unrealpak/package_compressed.py")

old_pak = "C:/Program Files (x86)/Steam/steamapps/common/Zedfest/KevinSpel/Content/Paks/LogicMods/Z_ModLoader_P.pak"
new_pak = "C:/Users/Mythical/Documents/GitHub/Interpose/modding_workspace/scripts/python/python_unrealpak/Z_ModLoader_P.pak"

if os.path.isfile(old_pak):
    os.remove(old_pak)
    
if os.path.isfile(new_pak):
    shutil.move(new_pak, old_pak)

subprocess.Popen(game_exe)

time.sleep(1)

screen_1_width =  -1920
screen_2_width =  1234
screen_2_length = 800

def find_window_by_title(window_title):
    hwnd = win32gui.FindWindow(None, window_title)
    return hwnd

def move_window(hwnd, left, top, width, height):
    win32gui.MoveWindow(hwnd, left, top, width, height, True)

window_title_to_find = "UE4SS Debugging Tools (OpenGL 3)"
hwnd = find_window_by_title(window_title_to_find)
move_window(hwnd, screen_1_width, 0, screen_2_width, screen_2_length)

time.sleep(999999)

sys.exit()
