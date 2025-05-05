
import moviepy.editor as mp
import speech_recognition as sr
import gdown

# Download the video using gdown
url = "https://drive.google.com/file/d/1PdAMHqHSBGGCV6HELPNwzKzX9-1WoX05/view?usp=sharing"
output = "geeksforgeeks.mp4"  # Choose your desired output filename

# Replace 'view?usp=sharing' with 'uc?id=' in the URL
file_id = url.split('/')[-2]
download_url = f"https://drive.google.com/uc?id={file_id}"

gdown.download(download_url, output, quiet=False)

# Load the downloaded video file
video = mp.VideoFileClip(output)  # Use the downloaded file path


# Extract the audio from the video
audio_file = video.audio
audio_file.write_audiofile("geeksforgeeks.wav")

# Initialize recognizer
r = sr.Recognizer()

# Load the audio file
with sr.AudioFile("geeksforgeeks.wav") as source:
    data = r.record(source)

# Convert speech to text
text = r.recognize_google(data)

# Print the text
print("\nThe resultant text from video is: \n")
print(text)