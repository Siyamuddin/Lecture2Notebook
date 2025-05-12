import os
from dotenv import load_dotenv

# ✅ Load the .env file before anything else
load_dotenv(dotenv_path="Secrete.env")

import nbformat as nbf
import yt_dlp
from faster_whisper import WhisperModel
from groq import Groq



def download_audio(youtube_url: str) -> str:
    output_path = "audio.%(ext)s"
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
            'preferredquality': '192',
        }],
        'quiet': False,  # 👈 Temporarily set this to False to see logs
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
    except Exception as e:
        print(f"yt_dlp download error: {e}")
        return None

    if not os.path.exists("audio.m4a"):
        print("Expected audio file not found after download.")
        return None

    return "audio.m4a"


def transcribe_audio(file_path: str) -> str:
    # Now initialize your models
    print(f"[DEBUG] transcribing audio file {file_path}")
    model = WhisperModel(os.getenv("WHISPER_MODEL"))
    segments, _ = model.transcribe(file_path)
    print(f"[DEBUG] transcribing finished")
    return " ".join([seg.text for seg in segments])

def generate_code(prompt: str) -> str:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant that reads Python lecture transcriptions, detects the lecture topics and generates clean, organized Python code examples. "
                    "Each topic explained by the professor (e.g., arrays, lambda functions, file handling, etc.) should have its own code block. "
                    "Only include the code examples that the professor explicitly gave while teaching, and format them clearly using comments to separate sections. "
                    "The output should be ready to use in Google Colab and suitable for beginner students to run and learn from."
                )
            },
            {
                "role": "user",
                "content": f"tThis is a video transcription of a Python lecture. Please extract all the example codes the professor provided and organize them by topic with commens:\n\n{prompt}"
            }
        ],
        model="llama-3.1-8b-instant",
    )
    return response.choices[0].message.content

def save_to_notebook(code: str, filename="generated_notebook.ipynb") -> str:
    print(f"[INFO] GENERATED_CODE: Saving started")
    nb = nbf.v4.new_notebook()
    nb.cells.append(nbf.v4.new_code_cell(code))
    with open(filename, 'w') as f:
        nbf.write(nb, f)
    return filename
