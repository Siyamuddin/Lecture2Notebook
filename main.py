from fastapi import FastAPI, HTTPException
from models import YouTubeRequest, YouTubeResponse
from auth import get_student_info
from utils import download_audio, transcribe_audio, generate_code, save_to_notebook
from fastapi.responses import FileResponse
import os

app = FastAPI()

@app.post("/generate-colab", response_model=YouTubeResponse)
async def generate_colab(req: YouTubeRequest):
    student_info = get_student_info(req.id, req.password)
    if not student_info:
        raise HTTPException(status_code=401, detail="Authentication failed. Only Sejong students are allowed.")

    try:
        audio_path = download_audio(req.youtube_url)
        transcript = transcribe_audio(audio_path)
        code = generate_code(transcript)
        notebook_path = save_to_notebook(code)

        os.remove(audio_path)

        return YouTubeResponse(
            student_name=student_info['name'],
            student_major=student_info['major'],
            message="Notebook generated successfully.",
            notebook_link=f"/download/{notebook_path}",
            transcript=transcript

        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = f"./{filename}"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found.")
    return FileResponse(path=file_path, media_type='application/octet-stream', filename=filename)
