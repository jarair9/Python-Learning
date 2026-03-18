# Permanent Memory 

import json
from mistralai.client import Mistral
from dotenv import load_dotenv
import os

load_dotenv()

file = "Agentic Coding/memory.json"
client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))


# Handle if file Not found
if not os.path.exists(file):
    # print("File Not found")
    with open("Agentic Coding/memory.json","w") as f:
        f.write(" ") # No content we need just need file to create

def load_memory():
    try:
        with open(file,"r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # print("Memory corrupted, starting fresh.")
        return []
    

def write_memory(history):
    with open(file,"w") as f:
        json.dump(history,f,indent=2)


conversation_list = load_memory()

def chatbot(text):

    conversation_list.append({"role": "user","content": text})
    response = client.chat.complete(
        model="mistral-small-2503",
        messages=conversation_list
    )

    reply = response.choices[0].message.content

    conversation_list.append({"role":"assistant","content": reply})
    write_memory(conversation_list)
    print("Assistant : ",reply)
    print()


while True:
    user = input("You: ")
    if user == "quit":
        break
    chatbot(user)