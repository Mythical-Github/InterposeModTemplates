import os
import subprocess

script_dir = os.path.dirname(os.path.abspath(__file__))

os.chdir(script_dir)

def open_file_browser(path):
    try:
        subprocess.Popen(['explorer', path])
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    directory_path = r"C:\Program Files (x86)\Steam\steamapps\common\Zedfest"
    open_file_browser(directory_path)
