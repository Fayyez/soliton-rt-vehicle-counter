import os
import sys

def create_venv_config():
    python_path = sys.executable
    python_folder_path = "/".join(sys.executable.split("/")[:-1]) if "/" in sys.executable else "\\".join(sys.executable.split("\\")[:-1])
    python_version = sys.version.split()[0]
    venv_dir = os.path.abspath("venv")
    with open("venv_config.txt", "w") as f:
        f.write(f"home = {python_folder_path}\n")
        f.write(f"include-system-site-packages = false\n")
        f.write(f"version = {python_version}\n")
        f.write(f"executable = {python_path}\n")
        f.write(f"command = {python_path} -m venv {venv_dir}\n")

import os
import subprocess
import sys

def activate_virtualenv():
    # Determine the platform
    platform = sys.platform

    # Define the virtual environment directory
    venv_dir = "venv"  # Replace with your virtual environment directory name if different

    # Construct the activation command based on the platform
    if platform.startswith("win"):
        activate_script = os.path.join(venv_dir, "Scripts", "activate")
    else:
        activate_script = os.path.join(venv_dir, "bin", "activate")

    # Check if the virtual environment exists
    if os.path.exists(activate_script):
        # Activate the virtual environment
        activate_command = f"{activate_script} && streamlit run main.py"
        subprocess.run(activate_command, shell=True)
    else:
        print(f"Virtual environment '{venv_dir}' not found. Please create it first.")

if __name__ == "__main__":
    # activate_virtualenv()
    create_venv_config()
