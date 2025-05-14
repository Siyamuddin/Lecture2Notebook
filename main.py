from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.background import BackgroundTask
from models import YouTubeRequest, YouTubeResponse
from auth import get_student_info
from utils import download_audio, transcribe_audio, generate_code, save_to_notebook, generate_class_summery, is_junior
from fastapi.responses import FileResponse
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate-colab", response_model=YouTubeResponse)
async def generate_colab(req: YouTubeRequest):
    if is_junior(req.id,23):
        raise HTTPException(status_code=401, detail="Authentication failed. Only Senior student can user this service.")

    student_info = get_student_info(req.id, req.password)
    if not student_info:
        raise HTTPException(status_code=401, detail="Authentication failed. Only Sejong students are allowed.")

    try:
        audio_path = download_audio(req.youtube_url)
        transcript = transcribe_audio(audio_path)
        code = generate_code(transcript)
        summary = generate_class_summery(transcript)
        notebook_path = save_to_notebook(code)

        os.remove(audio_path)

        return YouTubeResponse(
            student_name=student_info['name'],
            student_department=student_info['department'],
            student_major=student_info['major'],
            message="Notebook generated successfully.",
            notebook_link=notebook_path,
            class_summery=summary,
            transcript=transcript

        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = f"./{filename}"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found.")

    def cleanup():
        try:
            os.remove(file_path)
            print(f"{file_path} deleted successfully.")
        except Exception as e:
            print(f"Failed to delete {file_path}: {e}")

    return FileResponse(
        path=file_path,
        media_type='application/octet-stream',
        filename=filename,
        background=BackgroundTask(cleanup)
    )


