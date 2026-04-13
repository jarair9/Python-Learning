from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from AI_Tools2 import tool_registry, tools

load_dotenv()

client = OpenAI(
    api_key=os.getenv("MISTRAL_API_KEY"),
    base_url="https://api.mistral.ai/v1"
)

messages = [
    {"role": "system", "content": "You are a helpful AI agent that can use tools."}
]


def collect_stream(stream):
    """Collect all chunks and build a complete response"""
    content = ""
    tool_calls = []

    for chunk in stream:
        if not chunk.choices:
            continue

        delta = chunk.choices[0].delta
        finish_reason = chunk.choices[0].finish_reason

        #  collect text content as it streams
        if delta.content:
            print(delta.content, end="", flush=True)
            content += delta.content

        #  collect tool call chunks
        if delta.tool_calls:
            for tc in delta.tool_calls:
                # extend list if needed
                while len(tool_calls) <= tc.index:
                    tool_calls.append({
                        "id": "",
                        "type": "function",
                        "function": {"name": "", "arguments": ""}
                    })

                if tc.id:
                    tool_calls[tc.index]["id"] += tc.id
                if tc.function.name:
                    tool_calls[tc.index]["function"]["name"] += tc.function.name
                if tc.function.arguments:
                    tool_calls[tc.index]["function"]["arguments"] += tc.function.arguments

        if finish_reason:
            return content, tool_calls, finish_reason

    return content, tool_calls, "stop"


def runAgent(text):
    messages.append({"role": "user", "content": text})

    while True:
        #  stream=True
        stream = client.chat.completions.create(
            model="mistral-small-2503",
            messages=messages,
            tools=tools,
            stream=True
        )

        print("\n🤖 Assistant: ", end="")

        #  collect all chunks
        content, tool_calls, finish_reason = collect_stream(stream)

        #  AI finished — no tool calls
        if finish_reason != "tool_calls" or not tool_calls:
            print()  # new line
            return

        print()  # new line after streamed content

        #  add assistant message with tool calls
        messages.append({
            "role": "assistant",
            "content": content,
            "tool_calls": [
                {
                    "id": tc["id"],
                    "type": "function",
                    "function": {
                        "name": tc["function"]["name"],
                        "arguments": tc["function"]["arguments"]
                    }
                }
                for tc in tool_calls
            ]
        })

        #  run each tool and send results back
        for tc in tool_calls:
            tool_name = tc["function"]["name"]
            tool_args = json.loads(tc["function"]["arguments"])

            # print(f"\n🔧 Tool   : {tool_name}")
            # print(f"📥 Args   : {tool_args}")

            if tool_name in tool_registry:
                result = tool_registry[tool_name](**tool_args)
            else:
                result = f"❌ Unknown tool: {tool_name}"

            print(f"📤 Result : {result}")

            messages.append({
                "role": "tool",
                "tool_call_id": tc["id"],
                "content": str(result)
            })


while True:
    user = input("\nYou: ")
    if user.lower() == "quit":
        break
    runAgent(user)
    
"""



### What `collect_stream` does
```
chunk 1: delta.content = "The "
chunk 2: delta.content = "weather "
chunk 3: delta.content = "is..."
chunk 4: delta.tool_calls = [{name: "weat", arguments: ""}]
chunk 5: delta.tool_calls = [{name: "her_tool", arguments: '{"loc'}]
chunk 6: delta.tool_calls = [{name: "", arguments: 'ation": "Karachi"}']
chunk 7: finish_reason = "tool_calls"

collected:
  content    = "The weather is..."
  tool_calls = [{"name": "weather_tool", "arguments": '{"location": "Karachi"}'}]
```

Tool call chunks arrive in **pieces** — you must **concatenate** them together!

---

### What you'll see
```
You: what's the weather in Karachi?

🤖 Assistant: 
🔧 Tool   : weather_tool
📥 Args   : {'location': 'Karachi'}
📤 Result : {'temp_c': 32, ...}

🤖 Assistant: The current weather in Karachi is 32°C and sunny! ← streams word by word ✅"""