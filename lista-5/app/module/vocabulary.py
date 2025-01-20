import json
import bisect

class Vocabulary:
  #
  def __init__(self, filepath):
    self.vocabulary = []
    self.filepath = filepath
    self.updated = 0
    
  #
  def add(self, w):
    idx = self.get(w) 
    
    if idx is None:
      bisect.insort(self.vocabulary, (w, len(self.vocabulary))) # Inserção ordenada
      
      idx = self.get(w)
      self.updated += 1
      
    return idx
  
  #
  def get(self, w):
    for word, id in self.vocabulary: # Está ordenado
      if word == w:
        return str(id)
      
    return None
  
  #
  def get_all(self, w):
    terms_ids = []
    for word, id in self.vocabulary: # Está ordenado
      if w in word:
        terms_ids.append(id)
      
    return terms_ids
    
  #
  def load(self):
    # Safety
    if self.updated > 0:
      print(f'Não é possível carregar o vocabulário.\nExistem {self.updated} modificações a serem salvas.')
      return
    
    try:
      with open(self.filepath, 'r') as file: 
        self.vocabulary = json.load(file)['vocabulary']
        
      self.updated = 0
      print(f'Vocabulário: {len(self.vocabulary)} palavras')
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
        json.dump({"vocabulary": self.vocabulary}, file, indent=2)
        
      self.updated = 0
      print(f'Vocabulário salvo com {len(self.vocabulary)} palavras')
    except:
      print(f'Erro ao salvar arquivo: {self.filepath}')