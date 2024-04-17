import React, { useEffect } from 'react';
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition';

const VoiceRecorder = () => {
  const { transcript, resetTranscript, listening } = useSpeechRecognition();

  useEffect(() => {
    SpeechRecognition.startListening({ continuous: true });

    return () => {
      SpeechRecognition.stopListening();
    };
  }, []); // Run only once on component mount

  useEffect(() => {
    if (transcript.toLowerCase().includes('hey')) {
      sendDataToBackend(transcript);
      resetTranscript(); // Reset transcript after sending data
    }
  }, [transcript]); // Run when transcript changes

  const sendDataToBackend = async (data) => {
    try {
      // Replace 'your-backend-api-url' with your actual backend API endpoint
      const response = await fetch('http://127.0.0.1:5000/api', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ data })
      });

      if (response.ok) {
        console.log('Data sent to backend successfully');
      } else {
        console.error('Failed to send data to backend');
      }
    } catch (error) {
      console.error('Error sending data to backend:', error);
    }
  };

  return (
    <div>
      {listening ? (
        <p>Listening...
            <br/>
            {transcript}
        </p>
      ) : (
        <p>Speech recognition is not supported or allowed in this browser.</p>
      )}
    </div>
  );
};

export default VoiceRecorder;
