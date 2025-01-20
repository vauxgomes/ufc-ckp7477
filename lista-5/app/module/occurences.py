import json
import bisect

class Occurences:
  def __init__(self, filepath):
    self.occurences = {}
    self.filepath = filepath
    self.updated = 0
  
  #
  def get(self, term_id):
    return self.occurences.get(str(term_id), [])
    
  #
  def add(self, term_id, documment_id, freq):
    if term_id not in self.occurences:
      self.occurences[term_id] = []
      
    # Sem filtro de repeticão
    bisect.insort(self.occurences[term_id], (documment_id, freq)) # Inserção ordenada
    self.updated += 1
  
  #
  def load(self):
    # Safety
    if self.updated > 0:
      print(f'Não é possível carregar as ocorrências.\nExistem {self.updated} modificações a serem salvas.')
      return
    
    try:
      with open(self.filepath, 'r') as file: 
        self.occurences = json.load(file)
        
      self.updated = 0
      print(f'Ocorrências: {len(self.occurences)} palavras')
    except:
      print(f'Erro ao carregar arquivo: {self.filepath}')
  
  #
  def save(self):
    # Safety
    if self.updated == 0:
      print('Nada para salvar!')
      return
    
    try:
      with open(self.filepath, 'w') as file:
        json.dump(self.occurences, file, indent=2)
        
      self.updated = 0
      print(f'Ocorrências salvas com {len(self.occurences)} palavras')
    except:
      print(f'Erro ao salvar arquivo: {self.filepath}')