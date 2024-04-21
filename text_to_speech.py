from gtts import gTTS
from langdetect import detect
import pygame
import os

def text_to_speech(text):
    try:
        # Detect the language of the input text
        language = detect(text)

        tts = gTTS(text=text, lang=language)
        file_path = 'temp.mp3'
        tts.save(file_path)

        # Play the audio using pygame
        if file_path:
            pygame.init()
            pygame.mixer.init()
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()

            # Wait until playback finishes
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            # Clean up temporary file
            os.remove(file_path)
        
    except Exception as e:
        print(f"Error: {e}")

# Example usage
if __name__ == '__main__':
    text_to_speak = "Hello, how are you?"
    text_to_speech(text_to_speak)

