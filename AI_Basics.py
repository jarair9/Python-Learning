from openai import AsyncOpenAI
import asyncio
import os
from dotenv import load_dotenv
import openai
load_dotenv()


class llmclient:
   
    def __init__(self, client):
        self.client = client
    

    async def non_streaming_resposne(self) -> str:
       
        try:
            response = await self.client.chat.completions.create(
                model="mistralai/mistral-7b-instruct:free",  # Specify the model to use
                messages=[{"role": "user", "content": "Explain gravity in one sentence."}]  # Define the user's message
            )
            return response.choices[0].message.content
        except openai.APIConnectionError:
            print("Server Error")

   
    async def streaming_response(self, User_text ) -> str:
        try:
            response = await self.client.chat.completions.create(
                model="z-ai/glm-4.5-air:free",  # Specify the model to use
                messages=[
                {"role": "system", "content": "You are a Helpful assistance like chatgpt help user in everything and response little short."},
                {"role": "user", "content": User_text}
            ], 
                stream=True  # Enable streaming mode
            )
        
        
            async for chunk in response:
                # Extract the content from the chunk
                content = chunk.choices[0].delta.content
                # Print the content if it is not None
                if content is not None:
                    print(content,end="")
            # Print a newline after the response is complete
            print()
        except openai.APIConnectionError:
            print("Server Error")
   
    async def usage_Stream(self):
       
        response = await self.client.chat.completions.create(
            model="mistralai/mistral-7b-instruct:free",  
            messages=[{"role": "user", "content": "Explain gravity in one sentence."}]  
        )
       
        if response and response.usage:
            
            prompt_tokens = response.usage.prompt_tokens
            completion_tokens = response.usage.completion_tokens
            total_tokens = response.usage.total_tokens
            # Print the token usage information
            print(f"Input Tokens: {prompt_tokens}")
            print(f"Output Tokens: {completion_tokens}")
            print(f"Total Tokens: {total_tokens}")
            print(f"Content: {response.choices[0].message.content}")
        else:
            print("Server error or empty response")

   
    async def usage_nStream(self):
       
       
        response = await self.client.chat.completions.create(
            model="mistralai/mistral-7b-instruct:free", 
            messages=[{"role": "user", "content": "Explain gravity in one sentence."}],  
            stream=True  
            )
        
        async for chunk in response:
            
            if chunk.usage is not None:
               
                print("\n" + "-" * 20)
                print(f"Final Input Tokens: {chunk.usage.prompt_tokens}")
                print(f"Final Output Tokens: {chunk.usage.completion_tokens}")
                print(f"Total Tokens: {chunk.usage.total_tokens}")


async def main():

    llm = llmclient(client=AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1", 
        api_key=os.getenv("OPENROUTER_API_KEY")  
    ))
    while True:
        user = input("\nYou: ")
        await llm.streaming_response(user)

asyncio.run(main())











