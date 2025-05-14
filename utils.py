import os
import uuid

from dotenv import load_dotenv

# ✅ Load the .env file before anything else
load_dotenv(dotenv_path="Secrete.env")

import nbformat as nbf
import yt_dlp
from groq import Groq



# def download_audio(youtube_url: str) -> str:
#     output_path = "audio.%(ext)s"
#     ydl_opts = {
#         'format': 'bestaudio/best',
#         'outtmpl': output_path,
#         'postprocessors': [{
#             'key': 'FFmpegExtractAudio',
#             'preferredcodec': 'm4a',
#             'preferredquality': '192',
#         }],
#         'quiet': False,  # 👈 Temporarily set this to False to see logs
#     }
#
#     try:
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             ydl.download([youtube_url])
#     except Exception as e:
#         print(f"yt_dlp download error: {e}")
#         return None
#
#     if not os.path.exists("audio.m4a"):
#         print("Expected audio file not found after download.")
#         return None
#
#     return "audio.m4a"

def download_audio(youtube_url: str) -> str:
    print("Downloading audio...")
    output_path = "audio.%(ext)s"
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '64',
        }],
        'quiet': True,
        'noplaylist': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
            print("Audio downloaded!")
        return "audio.mp3"
    except Exception as e:
        print(f"yt_dlp download error: {e}")
        return None

# def download_audio(youtube_url: str) -> str:
#     print("Downloading audio...")
#     output_path = "audio.%(ext)s"
#     ydl_opts = {
#         'format': 'bestaudio/best',
#         'outtmpl': output_path,
#         'postprocessors': [{
#             'key': 'FFmpegExtractAudio',
#             'preferredcodec': 'mp3',
#             'preferredquality': '64',  # Lower bitrate = smaller file
#         }],
#         'quiet': False,
#     }
#
#     try:
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             ydl.download([youtube_url])
#             print("Audio downloaded!")
#         return "audio.mp3"
#     except Exception as e:
#         print(f"yt_dlp download error: {e}")
#         return None


def transcribe_audio(file_path: str) -> str:
    print("Transcribing audio...")
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    print("File Path: "+file_path)
    filename = file_path

    with open(filename, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(filename, file.read()),
            model="whisper-large-v3",
            response_format="verbose_json",
        )
        print("Transcription completed!")

    return transcription.text

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

def save_to_notebook(code: str) -> str:
    filename = f"{uuid.uuid4().hex}.ipynb"
    print(f"[INFO] GENERATED_CODE: Saving started")
    nb = nbf.v4.new_notebook()
    nb.cells.append(nbf.v4.new_code_cell(code))
    with open(filename, 'w') as f:
        nbf.write(nb, f)
    return filename

def generate_class_summery(prompt: str) -> str:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant that generates summary from the transcription of a class lecture to help student understand the topic in less time."
                    "Make sure the summery is not more than 600 characters."
                    "Make sure to not miss any important topic"

                )
            },
            {
                "role": "user",
                "content": f"tThis is a video transcription of a Python lecture. Please generate the summary from the transcription of a class lecture to help student understand the topic better:\n\n{prompt}"
            }
        ],
        model="llama-3.1-8b-instant",
    )
    return response.choices[0].message.content

def is_junior(id_str: str,limit: int) -> bool:

    if len(id_str) < 2 or not id_str[:2].isdigit():
        return False  # Handle edge cases like too short or non-numeric start
    return int(id_str[:2]) > limit
