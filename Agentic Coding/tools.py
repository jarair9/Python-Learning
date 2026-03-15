import os
import shutil
from pathlib import Path
import requests

def get_current_directory():
    return str(Path.cwd())  # ✅ return string not Path object


def list_files_dirs(path="."):
    if not os.path.exists(path):
        return f"❌ Path '{path}' not found"
    
    items = os.listdir(path)
    result = []
    
    for item in items:
        full_path = os.path.join(path, item)
        if os.path.isdir(full_path):
            result.append(f"📁 Folder: {item}")
        elif os.path.isfile(full_path):
            result.append(f"📄 File: {item}")
    
    return "\n".join(result)  # ✅ return string instead of just printing


def read_file(file):
    try:
        with open(file, encoding="utf-8", mode="r") as f:
            return f.read()
    except FileNotFoundError:
        return f"❌ File '{file}' not found"


def write_file(file, content):
    try:
        with open(file, encoding="utf-8", mode="w") as f:
            f.write(content)
        return f"✅ Written to '{file}' successfully"  # ✅ return status
    except FileNotFoundError:
        return f"❌ File '{file}' not found"


def create_write_file(file, content=""):
    try:
        with open(file, encoding="utf-8", mode="w") as f:
            f.write(content)
        return f"✅ File '{file}' created successfully"  # ✅ return status
    except Exception as e:
        return f"❌ Error: {e}"


def delete_file(filename):
    if os.path.exists(filename):
        os.remove(filename)
        return f"✅ File '{filename}' deleted"  # ✅ return status
    return f"❌ File '{filename}' not found"


def rename_file(file, filename):
    if os.path.exists(file):
        os.rename(file, filename)
        return f"✅ Renamed '{file}' to '{filename}'"  # ✅ return status
    return f"❌ File '{file}' not found"

def remove_dir(dirname):
    if os.path.exists(dirname):
        os.removedirs(dirname)
        return f"📁{dirname} Sucessfully removed from you Curent Directory"
    return f"❌📁 folder '{dirname}' not found"


def weather_tool(location: str):
    base_url = "http://api.weatherapi.com/v1"
    api_key = os.getenv("WEATHER_API_KEY")
    url = f"{base_url}/current.json?key={api_key}&q={location}"
    response = requests.get(url)
    return response.json()
