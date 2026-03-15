import mistralai.client
import json
import os
from dotenv import load_dotenv

load_dotenv()

client = mistralai.client.Mistral(api_key=os.getenv("MISTRAL_API_KEY"))


def calculator(operation, a, b):
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        if b == 0:
            return "Error: division by zero"
        return a / b
    else:
        return "Unknown operation"

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Performs basic math: add, subtract, multiply, divide",
            "parameters": {
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "description": "add, subtract, multiply, or divide"
                    },
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"}
                },
                "required": ["operation", "a", "b"]
            }
        }
    }
]


def chatbot(user_message):
    messages = [{"role": "user", "content": user_message}]

    
    response = client.chat.complete(
        model="mistral-small-2503",
        messages=messages,
        tools=tools
    )

    
    if response.choices[0].finish_reason == "tool_calls":
        tool_call = response.choices[0].message.tool_calls[0]

        
        tool_name = tool_call.function.name
        tool_args = json.loads(tool_call.function.arguments)

        print(f"\n🔧 AI wants to call: {tool_name}")
        print(f"📥 With arguments: {tool_args}")

        
        if tool_name == "calculator":
            result = calculator(**tool_args)

        print(f"📤 Result: {result}")

        
        messages.append(response.choices[0].message)  
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": str(result)
        })

        
        final_response = client.chat.complete(
            model="mistral-small-2503",
            messages=messages,
            tools=tools
        )

        print(f"\nAssistant: {final_response.choices[0].message.content}")

    else:
        
        print(f"\nAssistant: {response.choices[0].message.content}")



while True:
    user = input("\nYou: ")
    if user.lower() == "quit":
        break
    chatbot(user)


# "type": "function",
# "function": {
# "name": "calculator",
# "description": "Performs basic math: add, subtract, multiply, divide",

# "parameters": {
#     "type": "object",        # always "object" — just means "a group of inputs"
    
#     "properties": {          # list of ALL inputs your function needs
        
#         "operation": {       # input 1 — matches function argument name exactly
#             "type": "string",           # text value
#             "description": "add, subtract, multiply, divide"  # AI reads this to understand what to pass
#         },
        
#         "a": {               # input 2
#             "type": "number",           # numeric value
#             "description": "a"
#         },
        
#         "b": {               # input 3
#             "type": "number",
#             "description": "b"
#         }
#     },
    
#     "required": ["operation", "a", "b"]  # ALL inputs must be provided
# }