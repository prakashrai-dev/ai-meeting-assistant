from dotenv import load_dotenv
from utils.audio_pro import process_input
from core.transcriber import transcribe_all
import os
load_dotenv()

# source = "https://www.youtube.com/watch?v=kYkZI3oj2W4"

# chunks = process_input(source)
# print(transcribe_all(chunks))  # english video 

print("KEY LOADED:", os.getenv("SARVAM_API_KEY"))
print("CWD:",os.getcwd())

source = "https://www.youtube.com/watch?v=FFEs5mfwOFg"
language = "hinglish" # hindi video => sarvam && english => whisper

chunks = process_input(source)
transcript = transcribe_all(chunks,language=language)
print("\n===TRANSCRIPT===\n")
print(transcript)



# language = "hinglish" # hindi video
# transcript = transcribe_all(chunks,language=language)
# print("\n===TRANSCRIPT===\n")
# print(transcript)