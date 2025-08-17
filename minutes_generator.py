import logging

from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class MinutesGenerator:
  def __init__(self, api_key, system_prompt, max_tokens) -> None:
    self.system_prompt = system_prompt
    self.client = OpenAI(api_key=api_key)
    self.model = 'gpt-4.1'
    self.token_limit = max_tokens
    
  def generate(self, meeting_transcription:str):
    if not meeting_transcription:
      logging.error("Transcription is null or empty")
      return
    
    meeting_chunks = [meeting_transcription[i:i + self.token_limit] for i in range(0, len(meeting_transcription), self.token_limit)]
    logging.info("Generating meeting minutes")
    
    with open('minutes.txt', 'w') as file:
      for chunk in meeting_chunks:
        response = self.client.chat.completions.create(model="gpt-4o",
          messages=[
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": chunk}
          ],
        max_tokens=self.token_limit,
        temperature=0.2)
        
        minutes_chunk = response.choices[0].message.content
        
        file.write(minutes_chunk)
    
    logging.info('Finished generating minutes')