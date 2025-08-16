
from tokenize import Token
from openai import audio
from minutes_generator import MinutesGenerator
import sys
import os
import argparse

SYSTEM_PROMPT = "Transforma todo o discurso direto do texto fornecido em discurso indireto, utilizando uma linguagem formal em português de Portugal. Inicia as frases com verbos como: 'informou', 'denotou', 'frisou', 'assegurou', 'referiu', 'declarou', 'indicou', entre outros. Mantém o tom formal e o estilo adequados a uma ata da assembleia municipal. Sempre que possível, evita repetições dos mesmos verbos consecutivamente e garante a clareza e objetividade do texto."

parser = argparse.ArgumentParser(description='Generate meeting minutes from a transcript file.')
parser.add_argument('path', type=str, help='Path to the transcript file')
parser.add_argument('minutes guidelines', type=str, help='Guidelines for the formation of the minutes', default=SYSTEM_PROMPT)

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
  
  minutes_generator = MinutesGenerator(SYSTEM_PROMPT, TOKEN_LIMIT)
  
  file_type = get_file_type(args.path)
  print(file_type)
  
  if file_type in AUDIO_TYPES:
    # transcribe the file first
    pass
    
  with open(args.path, 'r') as file:
    meeting_transcription = file.read()

  meeting_chunks = [meeting_transcription[i:i + TOKEN_LIMIT] for i in range(0, len(meeting_transcription), TOKEN_LIMIT)]
  minutes = []
  
  with open('minutes.txt', 'w') as file:
    for chunk in meeting_chunks:
      file.write(minutes_generator.generate(chunk))
  
  print('Finished writing the minutes')