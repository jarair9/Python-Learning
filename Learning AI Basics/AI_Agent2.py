from openai import OpenAI
# from mistralai.client import Mistral
from dotenv import load_dotenv
import os
import json
from AI_Tools2 import tool_registry, tools
import openai
load_dotenv()

# client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
client = OpenAI(api_key=os.getenv("MISTRAL_API_KEY"),base_url="https://api.mistral.ai/v1")

def runAgent(text):
    messages = [{"role": "user", "content": text}]

    while True:
        try:
            response = client.chat.completions.create(
                model="mistral-small-2503",
                messages=messages,
                tools=tools
                )
        except openai.APIConnectionError:
            print("Please check Your Internet Connection and try again :(")


        choice = response.choices[0]

        if choice.finish_reason != "tool_calls":
            print(f"\nAssistant: {choice.message.content}")
            return

        messages.append(choice.message)

        for tool_call in choice.message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)
            

            if tool_name in tool_registry:
                result = tool_registry[tool_name](**tool_args)
            else:
                result = f"Unknown tool: {tool_name}"

            print(f" Result  : {result}")

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })


while True:
    user = input("\nYou: ")
    if user.lower() == "quit":
        break
    runAgent(user)