import re
import json
import numpy as np
from collections import Counter

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# NLKT Downloads
nltk.download('stopwords') # Baixa as stopwords 
nltk.download('punkt') # Necessário para tokenizar as palavras

# NLKT Objects
stopwords = stopwords.words('portuguese')
stemmer = PorterStemmer()

from .vocabulary import Vocabulary
from .occurences import Occurences

#
def stemming(text):
  return [stemmer.stem(w.lower()) for w in re.sub(r'[^\w\s]', '', text).split()]
#
def remove_stopwords(words):
  return list(set(words).difference(stopwords))


#
class TFIDF:
  ''' 
  TF-IDF 
  
  Note: 
   - Em alguns pontos houveram conversões de valores para string devido a problemas de carregamento json
  '''
  
  def __init__(self, basepath=None):   
    if basepath is not None:
      self.filepaths = {
        'config': f'{basepath}/config.json',
        'vocabulary': f'{basepath}/vocabulary.json',
        'occurences': f'{basepath}/occurences.json'
      }
    
    self.vocabulary = None
    self.occurences = None    
    self.documents = {}
  
  #
  def get(self, w):
    term_id = str(self.vocabulary.get(w))
    return term_id, self.occurences.get(term_id)
    
  #
  def add(self, document_id, text):
    stemmed = stemming(re.sub(r"https?://\S+", "", text))
    words   = remove_stopwords(stemmed)
    counts  = Counter(stemmed)
    
    if len(words) == 0:
      return
    
    #
    self.documents[document_id] = counts.most_common(1)[0][1]
    
    for w in words:
      term_id = str(self.vocabulary.add(w))
      self.occurences.add(term_id, document_id, counts.get(w))
    
  #
  def tfidf(self, w, all=False):
    ''' 
      TF(t, d) = 
        (Número de vezes que o termo 't' aparece no documento 'd') / 
        (Palavra mais frequente no documento 'd')
        
      IDF(t) = log(
        (Número total de documentos no corpus) / 
        (Número de documentos que contêm o termo 't')
      )
        
      TF-IDF(t, d) = TF(t, d) * IDF(t) 
    '''
    
    w = stemming(w)[0]
    terms_ids = [self.vocabulary.get(w)] if not all else self.vocabulary.get_all(w)
    total_documents = len(self.documents)
    
    scores = []
    for term_id in terms_ids:
      occurences = self.occurences.get(term_id)  
      total_occurences = len(occurences)
      
      #
      for document_id, freq in occurences:
        tf  = freq / self.documents[str(document_id)]
        idf = np.log(total_documents / total_occurences)
        
        scores.append((tf * idf, int(document_id)))
    
    # Quanto maior, melhor
    return sorted(scores, key=lambda x: x[0], reverse=True)
  
  #
  def load(self):
    try:
      with open(self.filepaths['config'], 'r') as file: 
        config = json.load(file)
        self.documents = config['documents']
        # self.filepaths = config['filepaths']
    except:
      print(f'Erro ao carregar arquivo: {self.filepaths["config"]}')
      
    #
    self.vocabulary = Vocabulary(self.filepaths['vocabulary'])
    self.vocabulary.load()
    #
    self.occurences = Occurences(self.filepaths['occurences'])
    self.occurences.load()

  #
  def save(self):
    try:
      with open(self.filepaths['config'], 'w') as file:
        json.dump({
          "documents": self.documents,
          "filepaths": self.filepaths,
        }, file, indent=2)
      
      self.vocabulary.save()
      self.occurences.save()
    except:
      print(f'Erro ao salvar arquivo: {self.filepaths["config"]}')