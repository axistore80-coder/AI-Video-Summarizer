from youtube_transcript_api import YouTubeTranscriptApi 
from bs4 import BeautifulSoup
import requests
import re

class GetVideo:
    @staticmethod
    def Id(link):
        """Extracts the video ID from a YouTube video link."""

        pattern = r"(?:v=|youtu\.be/)([0-9A-Za-z_-]{11})"

        match = re.search(pattern, link)

        if match:
            return match.group(1)

        return None

    @staticmethod
    def title(link):
        """Gets the title of a YouTube video."""
        try:
            headers = {
                "User-Agent": "Mozilla/5.0"
            }

            r = requests.get(link, headers=headers, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")

            title = soup.find("meta", itemprop="name")["content"]
            return title

        except Exception:
            return "⚠️ Unable to fetch video title. Check the YouTube link."
        
    @staticmethod
    def transcript(link):
        """Gets the transcript of a YouTube video."""
        video_id = GetVideo.Id(link)

        if not video_id:
            return "⚠️ Invalid YouTube link."

        try:
            api = YouTubeTranscriptApi()

            transcript_list = api.list(video_id)

            try:
                transcript = transcript_list.find_transcript(['en'])
            except:
                transcript = transcript_list.find_generated_transcript(['en'])

            transcript_data = transcript.fetch()

            final_transcript = " ".join(snippet.text for snippet in transcript_data)

            return final_transcript

        except Exception as e:
            return f"⚠️ Transcript error: {e}"

    @staticmethod
    def transcript_time(link):
        """Gets transcript with timestamps."""
        video_id = GetVideo.Id(link)

        if not video_id:
            return "⚠️ Invalid YouTube link."

        try:
            api = YouTubeTranscriptApi()

            transcript_list = api.list(video_id)
            transcript = transcript_list.find_transcript(['en'])
            transcript_data = transcript.fetch()

            final_transcript = ""

            for snippet in transcript_data:
                final_transcript += snippet.text

                seconds = int(snippet.start)

                hours = seconds // 3600
                minutes = (seconds % 3600) // 60
                sec = seconds % 60

                timestamp = f"{hours:02d}:{minutes:02d}:{sec:02d}"

                final_transcript += f' (time:{timestamp}) '

            return final_transcript

        except Exception as e:
            return f"⚠️ Transcript error: {e}"