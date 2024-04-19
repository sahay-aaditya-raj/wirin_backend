import speech_recognition as sr

# Create a Recognizer instance
recognizer = sr.Recognizer()

# Use the microphone as source with increased timeout
with sr.Microphone() as source:
    print("Speak something...")
    
    # Adjust the timeout (in seconds) as needed (e.g., 5 seconds)
    recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise (optional)
    
    try:
        # Listen for audio with an increased timeout (e.g., 5 seconds)
        audio = recognizer.listen(source, timeout=5)
        
        print("Recognizing...")
        # Recognize speech using Google Speech Recognition
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
    except sr.RequestError as e:
        print(f"Error occurred; {e}")
    except sr.WaitTimeoutError:
        print("No audio detected within the specified timeout.")
