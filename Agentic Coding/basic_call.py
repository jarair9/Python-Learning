import openai
from dotenv import load_dotenv
import os


load_dotenv()


def generate_response(text):
    client = openai.OpenAI(api_key=os.getenv("CEREBRAS_API_KEY"),base_url="https://api.cerebras.ai/v1")

    response = client.chat.completions.create(
    model="gpt-oss-120b",
    messages=[
        {"role": "user", "content": text,}
    ])

    print(response.choices[0].message.content)
    


def generate_str_response(text):
    client = openai.OpenAI(api_key=os.getenv("CEREBRAS_API_KEY"),base_url="https://api.cerebras.ai/v1")

    response = client.chat.completions.create(
    model="gpt-oss-120b",
    messages=[
        {"role": "user", "content": text,}
    ],
    stream=True
)
    for chunks in response:
        delta = chunks.choices[0].delta.content
        if delta is not None:
            print(delta)


generate_str_response("hello")
