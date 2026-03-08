import asyncio
import io
import subprocess
import shutil
import tempfile
import os
import concurrent.futures
from typing import AsyncIterator, Iterator, Optional
import pygame
pygame.mixer.init()


class EdgeTTSStream:
    """
    Streams audio using Microsoft Edge TTS (free, no API key).
    Voices: en-US-AriaNeural, en-US-GuyNeural, en-GB-SoniaNeural, etc.
    Install: pip install edge-tts pygame
    """

    def __init__(self, voice: str = "en-US-AriaNeural", rate: str = "+0%", volume: str = "+0%"):
        self.voice = voice
        self.rate = rate
        self.volume = volume

    async def astream_bytes(self, text: str) -> AsyncIterator[bytes]:
        """Yield raw MP3 chunks as they arrive (async, true streaming)."""
        import edge_tts
        communicate = edge_tts.Communicate(text, self.voice, rate=self.rate, volume=self.volume)
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                yield chunk["data"]

    def stream_bytes(self, text: str) -> Iterator[bytes]:
        try:
            asyncio.get_running_loop()
            return self._stream_in_thread(text)
        except RuntimeError:
            return self._stream_sync(text)

    def _stream_sync(self, text: str) -> Iterator[bytes]:
        async def _collect():
            return [chunk async for chunk in self.astream_bytes(text)]
        return iter(asyncio.run(_collect()))

    def _stream_in_thread(self, text: str) -> Iterator[bytes]:
        def _run():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                async def _collect():
                    return [chunk async for chunk in self.astream_bytes(text)]
                return loop.run_until_complete(_collect())
            finally:
                loop.close()

        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            chunks = pool.submit(_run).result()
        return iter(chunks)

    def speak(self, text: str, output_file: Optional[str] = None):
        """Stream TTS audio and play it. Saves to output_file if given."""
        audio_data = b"".join(self.stream_bytes(text))

        if not audio_data:
            print("[TTS] Warning: received empty audio data.")
            return

        if output_file:
            with open(output_file, "wb") as f:
                f.write(audio_data)
            print(f"[TTS] Saved to {output_file}")
            self._play_pygame(output_file)          # ← play the saved file
        else:
            # pygame needs a real file path to seek MP3 — use a temp file
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                f.write(audio_data)
                tmp_path = f.name
            try:
                played = self._play_pygame(tmp_path)
                if not played:
                    played = self._play_ffplay(tmp_path)
                if not played:
                    fallback = "tts_output.mp3"
                    with open(fallback, "wb") as ff:
                        ff.write(audio_data)
                    print(f"[TTS] No player found — saved to {fallback}")
            finally:
                try:
                    os.unlink(tmp_path)
                except Exception:
                    pass

    @staticmethod
    def _play_pygame(mp3_path: str) -> bool:
        """
        Play MP3 via pygame.mixer.music (not Sound — music handles MP3 properly).
        Blocks until playback is complete.
        """
        try:
            pygame.mixer.music.load(mp3_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():    # ← WAIT until done
                pygame.time.Clock().tick(10)
            return True
        except Exception as e:
            print(f"[TTS] pygame error: {e}")
            return False

    @staticmethod
    def _play_ffplay(mp3_path: str) -> bool:
        """Fallback: play via ffplay (ships with ffmpeg)."""
        if not shutil.which("ffplay"):
            return False
        try:
            subprocess.run(
                ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", mp3_path],
                check=True,
            )
            return True
        except subprocess.CalledProcessError as e:
            print(f"[TTS] ffplay error: {e}")
            return False


if __name__ == "__main__":
    tts = EdgeTTSStream(voice="en-US-AriaNeural")
    tts.speak("Most people, when they think about it, say the screaming. It sounds more violent. More threatening. But study after study shows the opposite is true. Being ignored — truly, deliberately ignored — activates the same neural pathways as physical pain. The same pathways. Your brain doesn't distinguish between being punched and being frozen out by someone you love. It registers both as damage.", output_file="output.mp3")