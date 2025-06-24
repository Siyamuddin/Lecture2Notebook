from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.background import BackgroundTask
from models import YouTubeRequest, YouTubeResponse
from auth import get_student_info
from utils import download_audio, transcribe_audio, generate_code, save_to_notebook, generate_class_summery, is_junior
from fastapi.responses import FileResponse
import os
import threading
import time
import asyncio

app = FastAPI()

# Thread-safe data structures with locks
pending_files = {}  # filename: {"downloaded": False}
file_management_lock = threading.Lock()

# Rate limiting configuration with thread safety
user_request_log = {}  # user_id: [timestamps]
rate_limit_lock = threading.Lock()
RATE_LIMIT = 5  # max requests per user
WINDOW = 60     # seconds (1 minute)

# Memory cleanup configuration
CLEANUP_INTERVAL = 300  # 5 minutes
last_cleanup = time.time()


cookie_content = os.getenv("YT_COOKIES")
if cookie_content:
    with open("cookies.txt", "w") as f:
        f.write(cookie_content)



def cleanup_old_entries():
    """Periodically clean up old entries to prevent memory leaks"""
    global last_cleanup, user_request_log, pending_files
    
    with rate_limit_lock:
        now = time.time()
        # Clean up old rate limit entries
        for user_id in list(user_request_log.keys()):
            user_request_log[user_id] = [t for t in user_request_log[user_id] if now - t < WINDOW]
            if not user_request_log[user_id]:
                del user_request_log[user_id]
    
    with file_management_lock:
        # Clean up old pending files entries (files that should have been deleted)
        now = time.time()
        for filename in list(pending_files.keys()):
            if not os.path.exists(filename):
                pending_files.pop(filename, None)
    
    last_cleanup = now
    print(f"Memory cleanup completed at {time.strftime('%H:%M:%S')}")

def schedule_deletion(filename, delay=15):
    def delete_if_not_downloaded():
        time.sleep(delay)
        with file_management_lock:
            file_info = pending_files.get(filename)
            if file_info and not file_info["downloaded"]:
                try:
                    os.remove(filename)
                    print(f"{filename} auto-deleted after timeout.")
                except Exception as e:
                    print(f"Error auto-deleting {filename}: {e}")
                pending_files.pop(filename, None)
    threading.Thread(target=delete_if_not_downloaded, daemon=True).start()

def check_and_cleanup():
    """Check if cleanup is needed and perform it"""
    global last_cleanup
    if time.time() - last_cleanup > CLEANUP_INTERVAL:
        cleanup_old_entries()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate-colab", response_model=YouTubeResponse)
async def generate_colab(req: YouTubeRequest):
    # Periodic memory cleanup
    check_and_cleanup()
    
    # Thread-safe rate limiting check
    now = time.time()
    user_id = req.id

    with rate_limit_lock:
        # Clean up old timestamps for this user
        user_request_log.setdefault(user_id, [])
        user_request_log[user_id] = [t for t in user_request_log[user_id] if now - t < WINDOW]

        if len(user_request_log[user_id]) >= RATE_LIMIT:
            raise HTTPException(
                status_code=429, 
                detail=f"Rate limit exceeded. You can only generate {RATE_LIMIT} files per minute. Please wait before generating more files."
            )

        # Record this request
        user_request_log[user_id].append(now)

    # Existing authentication and processing logic
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
        #remove audio file
        os.remove(audio_path)
        
        notebook_path = save_to_notebook(code)

        # Thread-safe file tracking
        with file_management_lock:
            pending_files[notebook_path] = {"downloaded": False}
            schedule_deletion(notebook_path)

        expiry_seconds = 15
        expiry_timestamp = int(time.time()) + expiry_seconds

        return YouTubeResponse(
            student_name=student_info['name'],
            student_department=student_info['department'],
            student_major=student_info['major'],
            message="Notebook generated successfully.",
            notebook_link=notebook_path,
            class_summery=summary,
            transcript=transcript,
            expiry_timestamp=expiry_timestamp
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = f"./{filename}"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found.")

    # Thread-safe file status update
    with file_management_lock:
        file_info = pending_files.get(filename)
        if file_info:
            file_info["downloaded"] = True

    def cleanup():
        try:
            os.remove(file_path)
            print(f"{file_path} deleted after download.")
        except Exception as e:
            print(f"Failed to delete {file_path}: {e}")
        
        with file_management_lock:
            pending_files.pop(filename, None)

    return FileResponse(
        path=file_path,
        media_type='application/octet-stream',
        filename=filename,
        background=BackgroundTask(cleanup)
    )

# Startup event to initialize cleanup
@app.on_event("startup")
async def startup_event():
    print("Application started. Thread-safe rate limiting and file management enabled.")
    print(f"Rate limit: {RATE_LIMIT} requests per {WINDOW} seconds per user")
    print(f"Memory cleanup interval: {CLEANUP_INTERVAL} seconds")


