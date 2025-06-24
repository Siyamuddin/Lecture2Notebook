from pydantic import BaseModel

class YouTubeRequest(BaseModel):
    id: str
    password: str
    youtube_url: str

class YouTubeResponse(BaseModel):
    student_name: str
    student_department: str
    student_major: str
    message: str
    notebook_link: str
    class_summery: str
    transcript: str
    expiry_timestamp: int  # Unix timestamp when the file will expire

