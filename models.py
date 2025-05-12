from pydantic import BaseModel

class YouTubeRequest(BaseModel):
    id: str
    password: str
    youtube_url: str

class YouTubeResponse(BaseModel):
    student_name: str
    student_major: str
    message: str
    notebook_link: str
    transcript: str

