import os
import sys
import json
import time
import glob
import psutil
import shutil
import msvcrt
import subprocess


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)


SETTINGS_JSON = f"{SCRIPT_DIR}/settings.json"


with open(SETTINGS_JSON) as file:
    json_data = json.load(file)


WINDOW_TITLE = json_data["window_title"]
os.system(f"title {WINDOW_TITLE}")


def print_possible_commands():
    print("""
Usage: python main.py <action>

Available Actions:
- run_ide or 0
- run_fmodel or 1
- run_blender or 2
- open_game_dir or 3
- open_uproject_dir or 4
- test_mods_cooked or 5
- test_mods_data_asset or 6
""")


if len(sys.argv) != 2:
    print_possible_commands()
    
    msvcrt.getch()
    
    sys.exit(1)

action = sys.argv[1]

def run_app(application_path):
    try:
        subprocess.Popen(application_path)
    except Exception as e:
        print("An error occurred:", e)
        

def is_process_running(process_name):
    for proc in psutil.process_iter():
        try:
            if process_name.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


def open_dir_in_file_browser(path):
    try:
        if path != "":
            subprocess.Popen(['explorer', path])
        else:
            raise ValueError("Path variable is empty.")
    except Exception as e:
        print("An error occurred:", e)


def run_blender():
    run_app(json_data["paths"]["blender_exe"])


def run_ide():
    run_app(json_data["paths"]["ide_exe"])


def run_fmodel():
    run_app(json_data["paths"]["fmodel_exe"])


def open_game_dir():
    game_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(json_data["paths"]["game_exe"])))))
    open_dir_in_file_browser(game_dir)
    

def open_uproject_dir():
    uproject_dir = os.path.dirname(os.path.abspath(json_data["paths"]["unreal_project_file"]))
    open_dir_in_file_browser(uproject_dir)    
    
    
def test_mods_data_asset():
    print("This is not currently implemented")
    return


def package_uproject():
    cook_output_dir = json_data["paths"]["output_dir"]
    uproject = json_data["paths"]["unreal_project_file"]
    engine_dir = json_data["paths"]["unreal_engine_dir"]
    
    os.chdir(engine_dir)
    os.system(f"Engine\Build\BatchFiles\RunUAT.bat BuildCookRun -project={uproject} -noP4 -platform=Win64 -clientconfig=Development -serverconfig=Development -cook -allmaps -stage -archive -archivedirectory={cook_output_dir}")


def copy_main_files():
    output_dir = json_data["paths"]["output_dir"]
    uproject = json_data["paths"]["unreal_project_file"]
    game_project_name = os.path.basename(uproject)
    uproject_name = game_project_name[:-9]
    print(uproject_name)
    content_dir = f"{output_dir}/WindowsNoEditor/{uproject_name}/Content"
    packing_dir = f"{SCRIPT_DIR}/mod_packaging/temp"
    if not os.path.isdir(packing_dir):
        os.mkdir(packing_dir)
        
    mod_list_length = (len(json_data["mod_pak_list"]))
    mod_list_max = mod_list_length
        
    for i in range (mod_list_max):
        mod_entry = json_data["mod_pak_list"][i]
        status_entry = mod_entry["status"]
        entry = mod_entry["name"]
        if status_entry == "on":
            mod_files_to_copy = f"{content_dir}/Mods/{entry}"
            place_to_copy_to = f"{packing_dir}/{entry}/{uproject_name}/Content/Mods/{entry}"
            shutil.copytree(mod_files_to_copy, place_to_copy_to)
        if status_entry == "off":
            uproject = json_data["paths"]["unreal_project_file"]
            game_project_name = os.path.basename(uproject)
            game_project_name = game_project_name[:-9]
            game_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(json_data["paths"]["game_exe"])))))
            game_paks_dir = f"{game_dir}/{game_project_name}/Content/Paks"
            mod_pak_type = mod_entry["pak_type"]
            inactive_pak_file = f"{game_paks_dir}/{mod_pak_type}/{entry}.pak"
            print(inactive_pak_file)
            if os.path.isfile(inactive_pak_file):
                os.remove(inactive_pak_file)
        
        
def copy_persistent_files():
    mod_files_to_copy = f"{SCRIPT_DIR}/mod_packaging/persistent_files"
    place_to_copy_to = f"{SCRIPT_DIR}/mod_packaging/temp"
    copy_tree((mod_files_to_copy), place_to_copy_to)


def copy_tree(src, dst, merge=True):
    if not os.path.exists(dst):
        os.makedirs(dst)
    
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)

        if os.path.isdir(s):
            copy_tree(s, d, merge)
        else:
            if merge and os.path.exists(d):
                base, ext = os.path.splitext(d)
                counter = 1
                while os.path.exists(d):
                    d = f"{base}_{counter}{ext}"
                    counter += 1

            shutil.copy2(s, d)


def cleanup_files():
    packing_dir = f"{SCRIPT_DIR}/mod_packaging/temp"
    if os.path.isdir(packing_dir):
        shutil.rmtree(packing_dir)


def make_and_move_paks():
    repak_pak_ver = json_data["repak_pak_ver"]
    repak_exe = json_data["paths"]["repak_exe"]
    unreal_engine_dir = json_data["paths"]["unreal_engine_dir"]
    unrealpak_exe = f"{unreal_engine_dir}/Engine/Binaries/Win64/UnrealPak.exe"
    packing_dir = f"{SCRIPT_DIR}/mod_packaging/temp"
    subfolders = [ f.path for f in os.scandir(packing_dir) if f.is_dir() ]
    for folder in subfolders:

        pak_name = os.path.basename(folder)
        pak_file = f"{pak_name}.pak"

        command = [repak_exe, "pack", "--version", repak_pak_ver, folder]
        
        try:
            subprocess.run(command, check=True)
            print(f"{pak_file} created successfully.")
            
            uproject = json_data["paths"]["unreal_project_file"]
            game_project_name = os.path.basename(uproject)
            game_project_name = game_project_name[:-9]
            game_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(json_data["paths"]["game_exe"])))))
            game_paks_dir = f"{game_dir}/{game_project_name}/Content/Paks"
            
            
            mod_list_length = (len(json_data["mod_pak_list"]))
            mod_list_max = mod_list_length
        
            for i in range (0, mod_list_max):
                mod_entry = json_data["mod_pak_list"][i]
                mod_name = mod_entry["name"]
                if mod_name == pak_name:
                    mod_pak_type = mod_entry["pak_type"]
                
                    old_pak = f"{game_paks_dir}/{mod_pak_type}/{pak_name}.pak"
                    new_pak = f"{packing_dir}/{pak_file}"
                    
                    if os.path.isfile(old_pak):
                        os.remove(old_pak)
                    shutil.copy(new_pak, old_pak)    

            
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")     


def kill_processes():
    process_list = json_data["process_kill_list"]
    for process in process_list:
        if is_process_running(process):
            os.system("taskkill /f /im " + process)
            

def run_game():
    launch_method = json_data["launch_method"]
    if launch_method == "win64_exe":
        game_win64_exe = json_data["paths"]["game_exe"]
        subprocess.Popen(f"{game_win64_exe} -NOSPLASH -fileopenlog")
    if launch_method == "steam":
        steam_app_id = json_data["steam_game_app_id"]
        os.system(f"start steam://rungameid/{steam_app_id}")      
    

def test_mods_cooked():
    cleanup_files()
    package_uproject()
    copy_main_files()
    copy_persistent_files()
    kill_processes()
    make_and_move_paks()
    cleanup_files()
    run_game()
    

def main():
    actions = {
        'run_ide': run_ide,
        'run_fmodel': run_fmodel,
        'run_blender': run_blender,
        'open_game_dir': open_game_dir,
        'open_uproject_dir': open_uproject_dir,
        'test_mods_cooked': test_mods_cooked,
        'test_mods_data_asset': test_mods_data_asset        
    }

    if action in actions:
        actions[action]()
    elif action.isdigit():
        index = int(action)
        if 0 <= index < len(actions):
            action_names = list(actions.keys())
            selected_action = action_names[index]
            actions[selected_action]()
        else:
            print_possible_commands()
    else:
        print_possible_commands()


if __name__ == "__main__":
    main()
    sys.exit()
