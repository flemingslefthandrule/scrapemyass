#!/usr/bin/env python

# please dont run, does not work yet

import os
import sys
import platform

project_folder = os.getcwd()

venv_name = "venv"

venv_path = os.path.join(project_folder, venv_name)

requirements_file = os.path.join(project_folder, "requirements.txt")

def activate_venv():
    if platform.system() == "Windows":
        command = f"{venv_path}\\Scripts\\Activate.ps1"
    else:
        command = f"source {venv_path}/bin/activate"
    os.system(command)

def deactivate_venv():
    command = "deactivate"
    os.system(command)

def install_requirements():
    command = f"pip install -r {requirements_file}"
    os.system(command)

if not os.path.exists(venv_path):
    print(f"virtual environment {venv_name} does not exist.\ncreating it...")
    if platform.system() == "Windows":
        command = f"python -m venv {venv_path}"
    else:
        command = f"python3 -m venv {venv_path}"
    os.system(command)