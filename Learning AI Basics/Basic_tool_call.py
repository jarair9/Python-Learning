# Simple Tool call


from mistralai.client import Mistral
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))


def weather_tool(location: str):
    base_url = "http://api.weatherapi.com/v1"
    api_key = os.getenv("WEATHER_API_KEY")
    url = f"{base_url}/current.json?key={api_key}&q={location}"
    response = requests.get(url)
    return response.json()

tool = {
    "type": "function",
    "function": {
        "name": "weather_tool",
        "description": "Get current weather information for a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city or location to get weather for e.g. Karachi, London"
                }
            },
            "required": ["location"]  
        }
    }
}

def chatbot(text):
    messages = [{"role": "user", "content": text}]

   
    response = client.chat.complete(
        model="mistral-small-2503",
        messages=messages,
        tools=[tool]
    )

    if response.choices[0].finish_reason == "tool_calls":
        tool_call = response.choices[0].message.tool_calls[0]
        tool_name = tool_call.function.name
        tool_args = json.loads(tool_call.function.arguments)  

        print(f"🔧 Calling: {tool_name} with {tool_args}")

      
        if tool_name == "weather_tool":
            result = weather_tool(**tool_args)

       
        messages.append({"role": "assistant", "content": "", "tool_calls": response.choices[0].message.tool_calls})
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result)  
        })

        
        final_response = client.chat.complete(
            model="mistral-small-2503",
            messages=messages,
            tools=[tool]
        )

        return final_response.choices[0].message.content  

    return response.choices[0].message.content


print(chatbot("What's the weather in Karachi?"))
