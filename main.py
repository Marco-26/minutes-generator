from tokenize import Token
from openai import audio
from minutes_generator import MinutesGenerator

from audio_transcriber.transcriber import Transcriber

import sys
import os
import argparse

SYSTEM_PROMPT = "Transforma todo o discurso direto do texto fornecido em discurso indireto, utilizando uma linguagem formal em português de Portugal. Inicia as frases com verbos como: 'informou', 'denotou', 'frisou', 'assegurou', 'referiu', 'declarou', 'indicou', entre outros. Mantém o tom formal e o estilo adequados a uma ata da assembleia municipal. Sempre que possível, evita repetições dos mesmos verbos consecutivamente e garante a clareza e objetividade do texto."

parser = argparse.ArgumentParser(description='Generate meeting minutes from a transcript file.')
parser.add_argument('path', type=str, help='Path to the transcript file')
parser.add_argument('--minutes guidelines', type=str, help='Guidelines for the formation of the minutes', default=SYSTEM_PROMPT)

TOKEN_LIMIT = 10000
AUDIO_TYPES = ['mp3', 'wav', 'mp4']

def get_file_type(filepath):
  ext = filepath.rsplit('.', 1)[-1].lower()
  return ext

if __name__ == "__main__":
  args = parser.parse_args()
  
  if not os.path.exists(args.path):
    print("File doesn't exist...")
    sys.exit()
  
  api_key = os.getenv('OPENAI_API_KEY')
  minutes_generator = MinutesGenerator(api_key, SYSTEM_PROMPT, TOKEN_LIMIT)
  
  file_type = get_file_type(args.path)
  
  meeting_transcription = ''
  
  if file_type in AUDIO_TYPES:
    transcriber = Transcriber(api_key, 'OpenAI')
    meeting_transcription = transcriber.transcribe(args.path)
  else:
    with open(args.path, 'r') as file:
      meeting_transcription = file.read()
      
  minutes_generator.generate(meeting_transcription)