# Python Lecture Video Processor

This project helps students and educators extract Python code examples and concise summaries from YouTube lecture videos. It downloads the audio from a YouTube video, transcribes it, uses AI to extract and organize code examples, and saves them into a Jupyter Notebook. It also generates a short summary of the lecture.

---

## Features

- **Download audio** from YouTube lecture videos.
- **Transcribe audio** to text using state-of-the-art AI (Whisper).
- **Extract and organize Python code examples** from lecture transcriptions.
- **Generate Jupyter Notebooks** with code examples grouped by topic.
- **Create concise lecture summaries** for quick review.
- **(Optional)**: Check if a student is a "junior" based on their ID.

---

## Requirements

- Python 3.8+
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [nbformat](https://nbformat.readthedocs.io/en/latest/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [Groq Python SDK](https://github.com/groq/groq-python)
- [FastAPI](https://fastapi.tiangolo.com/) (if using as an API)
- FFmpeg (for audio processing, required by yt-dlp)

Install dependencies with:

```bash
pip install -r requirements.txt
```

---

## Setup

1. **Clone the repository:**

   ```bash
   git clone <your-repo-url>
   cd fastApiProject
   ```

2. **Set up environment variables:**

   Create a file named `Secrete.env` in the project root with your API keys:

   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

3. **Install FFmpeg:**

   - On macOS: `brew install ffmpeg`
   - On Ubuntu: `sudo apt-get install ffmpeg`
   - On Windows: [Download FFmpeg](https://ffmpeg.org/download.html) and add it to your PATH.

---

## Usage

### As a Python Script

You can use the utility functions in `utils.py` directly in your own scripts or notebooks. Example:

```python
from utils import download_audio, transcribe_audio, generate_code, save_to_notebook, generate_class_summery

# Step 1: Download audio from YouTube
audio_file = download_audio("https://www.youtube.com/watch?v=example")

# Step 2: Transcribe audio
transcription = transcribe_audio(audio_file)

# Step 3: Extract code examples
code = generate_code(transcription)

# Step 4: Save code to Jupyter Notebook
notebook_file = save_to_notebook(code)

# Step 5: Generate summary
summary = generate_class_summery(transcription)
```

### As an API

If you have a FastAPI app (e.g., in `main.py`), run:

```bash
uvicorn main:app --reload
```

Then use the provided endpoints (see your API docs at `http://127.0.0.1:8000/docs`).

---

## File Structure

```
fastApiProject/
  ├── auth.py
  ├── Dockerfile
  ├── main.py
  ├── models.py
  ├── README.md
  ├── requirements.txt
  ├── test_main.http
  ├── utils.py
```

---

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## License

[MIT](LICENSE)

---

## Acknowledgements

- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [Groq](https://groq.com/)
- [OpenAI Whisper](https://github.com/openai/whisper)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Jupyter](https://jupyter.org/)

