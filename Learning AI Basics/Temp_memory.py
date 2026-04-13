# Temperary Memory
# This is Session whise memory if User termenate the terminal the memory vanished.
# It is good and simple chat for where you need little talk with AI or Ask Questions.
# It also consume Little token or context window for AN AI.


import openai
from dotenv import load_dotenv
import os

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("CEREBRAS_API_KEY"),base_url="https://api.cerebras.ai/v1")

conversation_list = [] 

def generate_response(text):
    conversation_list.append({"role": "user", "content": text})
    try:
        response = client.chat.completions.create(
            model="gpt-oss-120b",
            messages=conversation_list
        )
    except openai.RateLimitError:
        print("Rate limit exceeded — try again later.")
        conversation_list.pop()  
        return
    except openai.APIConnectionError:
        print("Check Your Connection and try again")
        return               

    reply = response.choices[0].message.content

    
    conversation_list.append({"role": "assistant", "content": reply})  
    
    print(f"AI: {reply}")

# Chat loop

while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break
    generate_response(user_input)