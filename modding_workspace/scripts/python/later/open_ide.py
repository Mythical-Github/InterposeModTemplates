import subprocess

def open_application(application_path):
    try:
        subprocess.Popen(application_path)
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    notepad_path = r"C:\Program Files\Notepad++\notepad++.exe"
    open_application(notepad_path)
