import sys
import os

def create_venv_config():
    python_path = sys.executable
    python_folder_path = "/".join(sys.executable.split("/")[:-1]) if "/" in sys.executable else "\\".join(sys.executable.split("\\")[:-1])
    python_version = sys.version.split()[0]
    venv_dir = os.path.abspath("venv")
    with open("venv/pyvenv.cfg", "w") as f:
        f.write(f"home = {python_folder_path}\n")
        f.write(f"include-system-site-packages = false\n")
        f.write(f"version = {python_version}\n")
        f.write(f"executable = {python_path}\n")
        f.write(f"command = {python_path} -m venv {venv_dir}\n")

if __name__ == "__main__":
    create_venv_config()