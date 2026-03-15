from mistralai.client import Mistral
from dotenv import load_dotenv
import os
import json

from tools import (
    get_current_directory,
    list_files_dirs,
    read_file,
    write_file,
    create_write_file,
    delete_file,
    rename_file,
    remove_dir,
    weather_tool
)

load_dotenv()
client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

tool_registry = {
    "get_current_directory": get_current_directory,
    "list_files_dirs":       list_files_dirs,
    "read_file":             read_file,
    "write_file":            write_file,
    "create_write_file":     create_write_file,
    "delete_file":           delete_file,
    "rename_file":           rename_file,
    "remove_dir":            remove_dir,
    "weather_tool":          weather_tool
}

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_directory",
            "description": "Returns the current working directory path",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_files_dirs",
            "description": "Lists all files and folders in a given directory",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Directory path to list. Defaults to current directory"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Reads and returns the content of a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "file": {"type": "string", "description": "Path to the file to read e.g. notes.txt"}
                },
                "required": ["file"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Writes content to an existing file (overwrites)",
            "parameters": {
                "type": "object",
                "properties": {
                    "file":    {"type": "string", "description": "Path to the file"},
                    "content": {"type": "string", "description": "Content to write into the file"}
                },
                "required": ["file", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_write_file",
            "description": "Creates a new file and writes content to it",
            "parameters": {
                "type": "object",
                "properties": {
                    "file":    {"type": "string", "description": "Name of the file to create e.g. hello.txt"},
                    "content": {"type": "string", "description": "Content to write in the file"}
                },
                "required": ["file"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_file",
            "description": "Deletes a file permanently",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "Name of the file to delete"}
                },
                "required": ["filename"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "rename_file",
            "description": "Renames or moves a file to a new name or path",
            "parameters": {
                "type": "object",
                "properties": {
                    "file":     {"type": "string", "description": "Current file name or path"},
                    "filename": {"type": "string", "description": "New file name or path"}
                },
                "required": ["file", "filename"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "remove_dir",
            "description": "Deletes a directory",
            "parameters": {
                "type": "object",
                "properties": {
                    "dirname": {"type": "string", "description": "Directory name to delete"}
                },
                "required": ["dirname"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "weather_tool",
            "description": "Get current weather information for a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "City or location e.g. Karachi, London"}
                },
                "required": ["location"]
            }
        }
    }
]


def runAgent(text):
    messages = [{"role": "user", "content": text}]

    while True:  # ✅ loop so AI can call multiple tools
        response = client.chat.complete(
            model="mistral-small-2503",
            messages=messages,
            tools=tools
        )

        choice = response.choices[0]

        # ✅ AI is done — give final answer
        if choice.finish_reason != "tool_calls":
            print(f"\n🤖 Assistant: {choice.message.content}")
            return

        # ✅ AI wants tools — run them all
        messages.append(choice.message)

        for tool_call in choice.message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)  # ✅ json.loads not json.load

            print(f"\n🔧 Tool called : {tool_name}")
            print(f"📥 Arguments   : {tool_args}")

            if tool_name in tool_registry:
                result = tool_registry[tool_name](**tool_args)
            else:
                result = f"❌ Unknown tool: {tool_name}"

            print(f"📤 Result      : {result}")

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })
        # ✅ loop continues — AI reads result and decides what to do next


while True:
    user = input("\nYou: ")
    if user.lower() == "quit":
        break
    runAgent(user)