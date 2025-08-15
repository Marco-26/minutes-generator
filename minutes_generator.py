import os

from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

class MinutesGenerator:
  def __init__(self, system_prompt, max_tokens) -> None:
    self.system_prompt = system_prompt
    self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    self.model = 'gpt-4.1'
    self.token_limit = max_tokens
    
  def generate(self, token:str):
    if token == None:
      return
    
    response = self.client.chat.completions.create(model="gpt-4o",
      messages=[
        {"role": "system", "content": self.system_prompt},
        {"role": "user", "content": token}
      ],
    max_tokens=self.token_limit,
    temperature=0.2)
    
    return response.choices[0].message.content