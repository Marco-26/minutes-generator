from minutes_generator import MinutesGenerator

system_prompt = "Transforma todo o discurso direto do texto fornecido em discurso indireto, utilizando uma linguagem formal em português de Portugal. Inicia as frases com verbos como: 'informou', 'denotou', 'frisou', 'assegurou', 'referiu', 'declarou', 'indicou', entre outros. Mantém o tom formal e o estilo adequados a uma ata da assembleia municipal. Sempre que possível, evita repetições dos mesmos verbos consecutivamente e garante a clareza e objetividade do texto."

token_limit = 10000
minutes_generator = MinutesGenerator(system_prompt, token_limit)

if __name__ == "__main__":
  with open('transcript.txt', 'r') as file:
    meeting_transcription = file.read()

  meeting_chunks = [meeting_transcription[i:i + token_limit] for i in range(0, len(meeting_transcription), token_limit)]
  for i, chunk in enumerate(meeting_chunks):
    minutes = minutes_generator.generate(chunk)
    print(f'Minutes from chunk {i}: {minutes}')
  