import sys
import shutil
import pathlib
import subprocess


print("py build file started")


old_dll = r"C:\Program Files (x86)\Steam\steamapps\common\EscapeTheBackrooms\EscapeTheBackrooms\Binaries\Win64\xinput1_3.dll"
new_dll = r"C:\Users\Mythical\Documents\GitHub\RE-UE4SS\Output\ue4ss\Binaries\x64\Debug\xinput1_3.dll"
game_exe = r"C:\Program Files (x86)\Steam\steamapps\common\EscapeTheBackrooms\EscapeTheBackrooms\Binaries\Win64\Backrooms-Win64-Shipping.exe"


if pathlib.Path(new_dll).is_file():
    if pathlib.Path(old_dll).is_file():
        pathlib.Path(old_dll).unlink()
    shutil.copy(new_dll, old_dll)


subprocess.Popen(game_exe)


print("py build file closing")


sys.exit()
