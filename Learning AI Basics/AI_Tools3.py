import os
import shutil
from pathlib import Path
import requests

tools = []
tool_registry = {}


def prop(type, description):
    return {"type": type, "description": description}

# This is complex decorator 


# We take Three args 
# We define Another Function that same function and we take Function
# Adding Tools in tool registry
# Putting or Appending the Core tool skeleton or definition to Tool 

def tool(description, properties={}, required=[]):
    def wrapper(func):
        tool_registry[func.__name__] = func
        tools.append({
            "type": "function",
            "function": {
                "name": func.__name__,
                "description": description,
                "parameters": {              #  inside function
                    "type": "object",
                    "properties": properties,
                    "required": required
                }
            }
        })
        return func # return and Run fuction to get all above Arges
    return wrapper # putting or Appending to Variables


@tool("Return the current working directory")
def get_current_directory():
    return str(Path.cwd())


@tool(
    description = "List files and folders in a directory",
    properties  = {"path": prop("string", "Directory path to list")},
)
def list_files_dirs(path="."):
    if not os.path.exists(path):
        return f"❌ Path '{path}' not found"
    result = []
    for item in os.listdir(path):
        full_path = os.path.join(path, item)
        prefix = "📁 Folder" if os.path.isdir(full_path) else "📄 File"
        result.append(f"{prefix}: {item}")
    return "\n".join(result)


@tool(
    description = "Reads and returns the content of a file",
    properties  = {"file": prop("string", "Path to the file e.g. notes.txt")},
    required    = ["file"]
)
def read_file(file):
    try:
        with open(file, encoding="utf-8", mode="r") as f:
            return f.read()
    except FileNotFoundError:
        return f"❌ File '{file}' not found"


@tool(
    description = "Write content to a file",
    properties  = {
        "file":    prop("string", "Path to the file e.g. notes.txt"),  # "string" not "file"
        "content": prop("string", "Content to write to the file")
    },
    required    = ["file", "content"]
)
def write_file(file, content):
    try:
        with open(file, encoding="utf-8", mode="w") as f:
            f.write(content)
        return f"✅ Written to '{file}' successfully"
    except FileNotFoundError:
        return f"❌ File '{file}' not found"


@tool(
    description = "Create a new file and write content to it",
    properties  = {
        "file":    prop("string", "Path to the file e.g. notes.txt"),  #  "string"
        "content": prop("string", "Content to write to the file")
    },
    required    = ["file"]
)
def create_write_file(file, content=""):
    try:
        with open(file, encoding="utf-8", mode="w") as f:
            f.write(content)
        return f"✅ File '{file}' created successfully"
    except Exception as e:
        return f"❌ Error: {e}"


@tool(
    description = "Delete a file permanently",
    properties  = {"filename": prop("string", "Path to the file to delete")},  # ✅ matches function arg
    required    = ["filename"]
)
def delete_file(filename):
    if os.path.exists(filename):
        os.remove(filename)
        return f"✅ File '{filename}' deleted"
    return f"❌ File '{filename}' not found"


@tool(
    description = "Rename or move a file",
    properties  = {
        "file":     prop("string", "Current file name or path"),
        "filename": prop("string", "New file name or path")   # ✅ added missing property
    },
    required    = ["file", "filename"]
)
def rename_file(file, filename):
    if os.path.exists(file):
        os.rename(file, filename)
        return f"✅ Renamed '{file}' to '{filename}'"
    return f"❌ File '{file}' not found"


@tool(
    description = "Remove or delete a directory",
    properties  = {"dirname": prop("string", "Folder or directory name")},  #  use prop()
    required    = ["dirname"]
)
def remove_dir(dirname):
    if os.path.exists(dirname):
        shutil.rmtree(dirname)   #  rmtree handles non-empty dirs, removedirs doesn't
        return f"✅ Folder '{dirname}' removed successfully"
    return f"❌ Folder '{dirname}' not found"


@tool(
    description = "Create a new folder",
    properties  = {"folder_name": prop("string", "Folder name to create")},  #  underscore, string
    required    = ["folder_name"]
)
def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        return f"✅ Folder '{folder_name}' created successfully"  #  return on success
    return f"❌ Folder '{folder_name}' already exists"


