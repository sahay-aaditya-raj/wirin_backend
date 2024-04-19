import speech_recognition as sr

# Create a Recognizer instance
recognizer = sr.Recognizer()

# Use the microphone as source with increased timeout
def speech_to_text(streamlit_obj) -> str:
    """_summary_

    Args:
        streamlit_obj (streamlit object): streamlit object passed for displaying listening and recognising

    Returns:
        str: "Recognized text from speech input."
    """
    
    with sr.Microphone() as source:
        print("Speak something...")
        streamlit_obj.write("Speak! Listening...")
        # Adjust the timeout (in seconds) as needed (e.g., 5 seconds)
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise (optional)
        
        try:
            # Listen for audio with an increased timeout (e.g., 5 seconds)
            audio = recognizer.listen(source)
            
            # stramlit object to write
            streamlit_obj.write("Recognizing...")
            streamlit_obj.write("Recognizing...")
            print("Recognizing...")
            # Recognize speech using Google Speech Recognition
            text = recognizer.recognize_google(audio)
            return text
            
        except sr.UnknownValueError:
            print("Sorry, could not understand audio.")
            return None
        except sr.RequestError as e:
            print(f"Error occurred; {e}")
            return None
        except sr.WaitTimeoutError:
            print("No audio detected within the specified timeout.")
            return None
