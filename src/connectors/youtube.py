### Youtube connector 
### Video Link -> Json

from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI
from ..config import OPEN_AI

import json

class Chat():
    def __init__(self) -> None:
        self.conn = OpenAI(api_key=OPEN_AI)

    def jsonify(self, completion):
        content = completion.choices[0].message.to_dict()['content']

        if content.startswith('```json') and content.endswith('```'):
            content = content[7:-3].strip()

        ###  Include more options here in the future

        return json.loads(content)

    def translate_transcript(self, transcript):
        completion = self.conn.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
                "role": "system",

                "content": (
                    "You are a helpful assistant. Translate the following video transcript into a JSON format using metric units. "
                    "The JSON should include the following fields: "
                    "Name, description, cuisine, category, servings, preptime, cooktime, difficulty, list of steps, list of ingredients.")},

                {   "role": "user",
                    "content": transcript}])
        return self.jsonify(completion)


class Youtube():
    def __init__(self) -> None:
        pass

    def get_youtube_transcript(self, video_url):
        try:
            video_id = video_url.split('v=')[-1].split('&')[0]
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            transcript_text = ' '.join([item['text'] for item in transcript])
            return transcript_text
        except Exception as e:
            return str(e)



