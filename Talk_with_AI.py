from openai import OpenAI
import edge_tts
import os
from dotenv import load_dotenv
import speech_recognition as sr
# from playsound import playsound
import asyncio
import time  # Add this import

load_dotenv()

def listen():

    r = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            print("Listening...")
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
        
        text = r.recognize_google(audio)
        print(f"You said: {text}")
        return text
    
    except sr.WaitTimeoutError:
        print("Listening timeout. No speech detected.")
        return ""
    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""
    except sr.RequestError as e:
        print(f"Speech recognition error: {e}")
        return ""
    except Exception as e:
        print(f"Error: {e}")
        return ""

def cleanup():
    
    file = "output.mp3"
    try:
        if os.path.exists(file):
            os.remove(file)
        return True
    except Exception as e:
        print(f"Warning: Could not remove {file}: {e}")
        return False

def speak(text):
    
    if not text.strip():
        return
    
    try:
        # Generate speech
        asyncio.run(edge_tts.Communicate(text, "en-US-AriaNeural").save("output.mp3"))
        
        # Play the audio
        # playsound("output.mp3")
        
        # Clean up
        cleanup()
        
    except Exception as e:
        print(f"Error in speech synthesis: {e}")

def Openrouter(text):
    
    client = OpenAI(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1"
    )
    
    try:
        response = client.chat.completions.create(
            model="z-ai/glm-4.5-air:free",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Keep responses concise and natural for speech."},
                {"role": "user", "content": text}
            ],
            temperature=0.7,
            max_tokens=150  # Limit response length for speech
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"Error getting AI response: {e}")
        return "I'm having trouble connecting right now. Please try again."

def main():
   
    print("=" * 50)
    print("Welcome to Voice Assistant!")
    print("Say 'exit', 'quit', or 'stop' to end")
    print("=" * 50)
    
    # Initial cleanup
    cleanup()
    
    while True:
        user_input = listen()
        
        if not user_input:
            continue
            
        if user_input.lower() in ['exit', 'quit', 'stop', 'bye', 'goodbye']:
            speak("Goodbye! Have a great day!")
            break
        
        print(f"Processing---")
        response = Openrouter(user_input)
        print(f"Assistant: {response}")
        speak(response)

if __name__ == "__main__":
    main()





# import os
# from openai import OpenAI

# client = OpenAI(
#     base_url="https://router.huggingface.co/v1",
#     api_key=os.environ["HF_TOKEN"],
# )

# completion = client.chat.completions.create(
#     model="zai-org/GLM-4.7-Flash:novita",
#     messages=[
#         {
#             "role": "user",
#             "content": "What is the capital of France?"
#         }
#     ],
# )

# print(completion.choices[0].message)