import asyncio
import edge_tts
import pygame
import io

pygame.mixer.init()

async def speak(text):
    print("Generating speech...")

    # Collect audio chunks as they stream in
    audio_data = b""
    tts = edge_tts.Communicate(text, voice="en-US-AriaNeural")

    async for chunk in tts.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]   # add each chunk as it arrives

    # Play the audio
    print("Playing...")
    sound = pygame.mixer.Sound(io.BytesIO(audio_data))
    sound.play()

    # Wait until done
    while pygame.mixer.get_busy():
        pygame.time.Clock().tick(10)

    print("Done!")


asyncio.run(speak("Most people, when they think about it, say the screaming. It sounds more violent. More threatening. But study after study shows the opposite is true. Being ignored — truly, deliberately ignored — activates the same neural pathways as physical pain. The same pathways. Your brain doesn't distinguish between being punched and being frozen out by someone you love. It registers both as damage."))