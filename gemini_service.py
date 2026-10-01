import json
from google import genai
from google.genai import types
from ..config import get_settings
class GeminiService:
    def __init__(self):
        s=get_settings(); self.client=genai.Client(api_key=s.gemini_api_key) if s.gemini_api_key else None; self.model=s.gemini_model
    def generate(self,prompt,image=None,mime=None):
        if not self.client: raise RuntimeError('GEMINI_API_KEY not configured')
        content=[prompt]
        if image: content.append(types.Part.from_bytes(data=image,mime_type=mime or 'image/jpeg'))
        r=self.client.models.generate_content(model=self.model,contents=content,config=types.GenerateContentConfig(temperature=.35,response_mime_type='application/json'))
        return json.loads(r.text or '{}')
gemini=GeminiService()
