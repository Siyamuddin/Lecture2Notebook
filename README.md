# 🎓 Lecture2Notebook

Lecture2Notebook is an AI-powered full-stack web application that automatically converts Python lecture videos into structured Jupyter Notebooks. It helps students quickly review and practice code examples taught in class by generating well-organized code cells categorized by topic.

> ✨ Built for Sejong University students to streamline learning from lecture recordings.

---

## 🌐 Live Demo

🚀 *Coming soon...*

---

## 📸 Screenshots

### 🖥️ Frontend Interface
<!-- Insert screenshot of the frontend interface here -->
![Frontend UI](./screenshots/frontend-ui.png)

### 📤 Upload & Processing
<!-- Insert screenshot showing file upload and processing status -->
![Upload Example](./screenshots/upload-example.png)

### 📄 Final Jupyter Notebook Output
<!-- Insert screenshot showing generated notebook preview -->
![Notebook Output](./screenshots/notebook-output.png)

### 🔒 Authentication (Sejong ID)
<!-- Insert screenshot showing Sejong login integration -->
![Sejong Auth](./screenshots/sejong-auth.png)

---

## 📌 Features

- 🎤 **Automatic Speech Recognition** using Whisper to transcribe lecture audio.
- 🧠 **AI Code Extraction** using Groq API + LLaMA 3.1 to identify code examples.
- 📓 **Notebook Generation** with `nbformat`, structured by topic in separate code cells.
- 🧪 **Student-Friendly Output** that runs easily in Jupyter or Google Colab.
- 🔐 **Sejong University Authentication** using student ID & password.
- 🧰 **Modern Frontend** built with React.js and TypeScript.
- 🌐 **API-first Backend** using FastAPI and Supabase for authentication and storage.

---

## 🛠️ Tech Stack

**Frontend:**
- React.js
- TypeScript
- Tailwind CSS

**Backend:**
- Python
- FastAPI
- Whisper (ASR)
- Groq API (LLaMA 3.1)
- nbformat
- Supabase (Auth & DB)
- Docker

---


---

## 🔄 API Overview

### 🎙️ POST `/upload`
Upload a lecture video.

### 🔍 POST `/transcribe`
Transcribe the uploaded video using Whisper.

### 📤 POST `/generate-code`
Send transcription to LLaMA 3.1 via Groq API for code extraction.

### 🧾 POST `/create-notebook`
Generate Jupyter Notebook with topic-separated code cells.

> You can test all endpoints using Postman.

<!-- Add Postman screenshot -->
![Postman Example](./screenshots/postman-example.png)

---

## 🧪 How to Run Locally

### 1️⃣ Clone the repository

```bash
git clone https://github.com/Siyamuddin/Lecture2Notebook.git
cd Lecture2Notebook
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn main:app --reload
3️⃣ Frontend Setup
bash
Copy
Edit
cd ../frontend
npm install
npm run dev
📚 Acknowledgements
OpenAI Whisper

Groq + LLaMA 3.1

nbformat

Supabase

Sejong University

📌 Author
Siyam Uddin
👨‍💻 Computer Science Student @ Sejong University
🌐 Portfolio
🔗 LinkedIn | GitHub

