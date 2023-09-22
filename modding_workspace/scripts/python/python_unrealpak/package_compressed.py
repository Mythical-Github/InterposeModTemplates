import os
import sys
import subprocess



folder_path = r"C:/Users/Mythical/Documents/GitHub/Interpose/modding_workspace/scripts/python/python_unrealpak/Z_ModLoader_P"

filelist_txt = os.path.join(os.path.dirname(__file__), "filelist.txt")
with open(filelist_txt, "w") as file:
    file.write(f"{folder_path}//*.* ..//..//..//*.*")

unrealpak_exe = os.path.join(os.path.dirname(__file__), "UnrealPak.exe")
pak_file = f"{folder_path}.pak"

command = [unrealpak_exe, pak_file, "-create=filelist.txt", "-compress"]

try:
    subprocess.run(command, check=True)
    print(f"{pak_file} created successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error: {e}")
finally:
    os.remove(filelist_txt)
