from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Callable
from pathlib import Path

load_dotenv()

# ============ 1. TOOL REGISTRY (your pattern, cleaned) ============

class ToolBox:
    """Simple tool registry with decorator."""
    def __init__(self):
        self._tools: dict[str, Callable] = {}
        self.schemas: list = []
    
    def register(self, name: str = None, description: str = "", 
                 params: dict = None):
        def decorator(func: Callable) -> Callable:
            tool_name = name or func.__name__
            self._tools[tool_name] = func
            
            self.schemas.append({
                "type": "function",
                "function": {
                    "name": tool_name,
                    "description": description or func.__doc__ or tool_name,
                    "parameters": params or {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            })
            return func
        return decorator
    
    def run(self, name: str, args: dict) -> str:
        if name not in self._tools:
            return f"Tool '{name}' not found"
        try:
            result = self._tools[name](**args)
            return str(result) if result is not None else "Done"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_schemas(self) -> list:
        return self.schemas


# ============ 2. MEMORY (JSON persistence) ============

class ChatMemory:
    """Simple file-based memory with automatic save/load."""
    
    def __init__(self, filepath: str = "chat_history.json", max_turns: int = 20):
        self.filepath = Path(filepath)
        self.max_turns = max_turns  # Keep last N exchanges
        self.messages: list[dict] = []
        self._load()
    
    def _load(self):
        """Load from disk or start fresh."""
        if self.filepath.exists():
            try:
                with open(self.filepath, 'r') as f:
                    self.messages = json.load(f)
            except json.JSONDecodeError:
                self.messages = []  # Corrupted? Start over.
        else:
            # First run: add system prompt
            self.messages = [{
                "role": "system",
                "content": "You are a helpful AI agent. Use tools when needed."
            }]
            self._save()
    
    def _save(self):
        """Write to disk."""
        with open(self.filepath, 'w') as f:
            json.dump(self.messages, f, indent=2)
    
    def add(self, role: str, content: str = None, **kwargs):
        """Add message and auto-trim old ones."""
        msg = {"role": role, "content": content, **kwargs}
        # Remove None values
        msg = {k: v for k, v in msg.items() if v is not None}
        
        self.messages.append(msg)
        
        # Trim: keep system + last max_turns exchanges (user+assistant pairs)
        if len(self.messages) > self.max_turns * 2 + 1:
            system_msgs = [m for m in self.messages if m["role"] == "system"]
            others = [m for m in self.messages if m["role"] != "system"]
            self.messages = system_msgs + others[-(self.max_turns * 2):]
        
        self._save()
    
    def get(self) -> list[dict]:
        """Return messages for API."""
        return self.messages.copy()
    
    def clear(self):
        """Reset but keep system prompt."""
        system = [m for m in self.messages if m["role"] == "system"]
        self.messages = system
        self._save()


# ============ 3. AGENT (your logic, wrapped) ============

class StreamingAgent:
    """Your exact streaming logic, organized into a class."""
    
    def __init__(self, api_key: str, base_url: str = None, model: str = "mistral-small-2503"):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
        self.memory = ChatMemory()
        self.tools = ToolBox()
    
    def _collect_stream(self, stream):
        """Your collect_stream logic, unchanged."""
        content = ""
        tool_calls = []

        for chunk in stream:
            if not chunk.choices:
                continue

            delta = chunk.choices[0].delta
            finish_reason = chunk.choices[0].finish_reason

            # Stream text to user immediately
            if delta.content:
                print(delta.content, end="", flush=True)
                content += delta.content

            # Accumulate tool calls by index
            if delta.tool_calls:
                for tc in delta.tool_calls:
                    # Grow list if new index
                    while len(tool_calls) <= tc.index:
                        tool_calls.append({
                            "id": "",
                            "type": "function", 
                            "function": {"name": "", "arguments": ""}
                        })
                    
                    if tc.id:
                        tool_calls[tc.index]["id"] += tc.id
                    if tc.function and tc.function.name:
                        tool_calls[tc.index]["function"]["name"] += tc.function.name
                    if tc.function and tc.function.arguments:
                        tool_calls[tc.index]["function"]["arguments"] += tc.function.arguments

            if finish_reason:
                return content, tool_calls, finish_reason

        return content, tool_calls, "stop"
    
    def run(self, user_input: str):
        """Main loop: stream → tools → stream again."""
        self.memory.add("user", user_input)
        
        while True:
            # Create streaming request
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=self.memory.get(),
                tools=self.tools.get_schemas() if self.tools.schemas else None,
                stream=True
            )
            
            print("\n🤖 Assistant: ", end="")
            content, tool_calls, finish_reason = self._collect_stream(stream)
            
            # No tools? Done.
            if finish_reason != "tool_calls" or not tool_calls:
                print()  # newline
                self.memory.add("assistant", content)
                return content
            
            # Save assistant message with tool_calls
            print()  # newline after streamed content
            self.memory.add("assistant", content, tool_calls=[
                {
                    "id": tc["id"],
                    "type": "function",
                    "function": {
                        "name": tc["function"]["name"],
                        "arguments": tc["function"]["arguments"]
                    }
                }
                for tc in tool_calls
            ])
            
            # Execute tools
            for tc in tool_calls:
                name = tc["function"]["name"]
                args = json.loads(tc["function"]["arguments"])
                
                print(f"\n🔧 Tool: {name}({args})")
                result = self.tools.run(name, args)
                print(f"📤 Result: {result[:200]}")
                
                # Add tool result to memory
                self.memory.add("tool", str(result), tool_call_id=tc["id"], name=name)


# ============ 4. SETUP TOOLS ============

toolbox = ToolBox()

@toolbox.register(
    name="get_weather",
    description="Get weather for a location",
    params={
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "City name"}
        },
        "required": ["city"]
    }
)
def get_weather(city: str) -> str:
    return f"Sunny, 25°C in {city}"

@toolbox.register(
    name="calculate",
    description="Do math",
    params={
        "type": "object",
        "properties": {
            "expression": {"type": "string", "description": "Math expression like '2 + 2'"}
        },
        "required": ["expression"]
    }
)
def calculate(expression: str) -> str:
    try:
        return str(eval(expression))  # Safe in controlled env
    except:
        return "Invalid expression"


# ============ 5. RUN ============

if __name__ == "__main__":
    agent = StreamingAgent(
        api_key=os.getenv("MISTRAL_API_KEY"),
        base_url="https://api.mistral.ai/v1",
        model="mistral-small-2503"
    )
    agent.tools = toolbox  # Inject tools
    
    print("💬 Chat started. Type 'quit' to exit, 'clear' to reset memory.")
    
    while True:
        user = input("\nYou: ").strip()
        
        if user.lower() == "quit":
            break
        elif user.lower() == "clear":
            agent.memory.clear()
            print("🗑️ Memory cleared")
            continue
        
        agent.run(user)