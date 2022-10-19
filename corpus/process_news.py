import nltk
from nltk.tokenize import sent_tokenize
import spacy
from itertools import chain
import os
nlp = spacy.load("es_core_news_sm")
an_set = set()

def get_text(path):
  file = open(path, 'r', encoding= 'utf-8')
  text = file.read()
  file.close()
  return text

def add_to_set(path):
  text = get_text(path)
  sent = sent_tokenize(text)
  for s in sent:
    doc = nlp(s)
    for token in doc:
      if token.pos_ == 'ADJ':
          for related in chain(token.lefts, token.rights):
              if related.pos_ == 'NOUN':
                  pair = (str.lower(token.text), str.lower(related.text))
                  an_set.add(pair)

path = r'corpus\news'
for filename in os.listdir(path):
  f = os.path.join(path, filename)
  add_to_set(f)

path = r'corpus\spanish_corpus.txt'
with open(path, 'w') as f:
  for d in an_set:
    f.write(' '.join(d)+'\n')