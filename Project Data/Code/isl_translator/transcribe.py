import base64
import io
import speech_recognition as sr

def transcribe_audio(audio_data):
    # Decode the base64 audio data
    audio_data = audio_data.split(",")[1]  # Remove the metadata part
    audio_bytes = base64.b64decode(audio_data)
    
    # Save the audio to a temporary file
    audio_file = io.BytesIO(audio_bytes)
    
    # Use SpeechRecognition to transcribe the audio
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)  # Read the entire audio file
        try:
            transcribed_text = recognizer.recognize_google(audio)  # Use Google Web Speech API
            return transcribed_text
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return f"Could not request results from Google Speech Recognition service; {e}"
# def test_transcribe_audio():
#     # Record audio using SpeechRecognition
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Please say something:")
#         audio = recognizer.listen(source)
    
#     # Convert the audio to base64
#     audio_bytes = audio.get_wav_data()
#     audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
#     audio_data = f"data:audio/wav;base64,{audio_base64}"
    
#     # Transcribe the audio
#     transcribed_text = transcribe_audio(audio_data)
    
#     # Print the transcribed text
#     print("Transcribed Text:", transcribed_text)
    
#     # Assert the transcribed text (this is a placeholder, adjust as needed)
#     assert transcribed_text != "Could not understand audio"
#     assert "Could not request results from Google Speech Recognition service" not in transcribed_text
# test_transcribe_audio()


# import base64
# import io
# import torch
# import whisper
# import torchaudio
# from transformers import pipeline

# # Initialize deep learning models
# device = "cuda" if torch.cuda.is_available() else "cpu"

# # Load Whisper model for speech recognition
# whisper_model = whisper.load_model("medium").to(device)

# # Optional: Wav2Vec 2.0 as alternative
# # asr_pipeline = pipeline("automatic-speech-recognition", 
# #                        model="facebook/wav2vec2-base-960h",
# #                        device=device)

# def transcribe_audio(audio_data):
#     try:
#         # Decode base64 audio
#         header, encoded = audio_data.split(",", 1)
#         audio_bytes = base64.b64decode(encoded)
        
#         # Convert to audio tensor
#         audio_stream = io.BytesIO(audio_bytes)
#         waveform, sample_rate = torchaudio.load(audio_stream)
        
#         # Resample if necessary
#         if sample_rate != 16000:
#             resampler = torchaudio.transforms.Resample(
#                 orig_freq=sample_rate, 
#                 new_freq=16000
#             )
#             waveform = resampler(waveform)
        
#         # Convert to numpy array for Whisper
#         audio_np = waveform.squeeze().numpy()

#         # Transcribe with Whisper
#         result = whisper_model.transcribe(
#             audio_np,
#             language="en",
#             fp16=(device == "cuda"),
#             temperature=0.2
#         )
        
#         return result["text"]
    
#     except Exception as e:
#         return f"Transcription error: {str(e)}"

# # Example usage with improved error handling
# async def handle_audio_transcription(audio_data):
#     try:
#         # Preprocess audio chunk
#         if len(audio_data) < 1024:
#             return {"error": "Audio data too short"}
            
#         transcription = transcribe_audio(audio_data)
        
#         # Post-process transcription
#         cleaned_text = transcription.strip().lower()
        
#         return {"text": cleaned_text}
    
#     except ValueError as ve:
#         return {"error": f"Invalid audio format: {str(ve)}"}
#     except RuntimeError as re:
#         return {"error": f"GPU processing error: {str(re)}"}/7