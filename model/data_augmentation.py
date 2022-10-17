import nltk
from nltk.corpus import wordnet as wn
nltk.download('wordnet')
nltk.download('omw-1.4')

def get_syn(word):
  synonyms = set()
  for syn in wn.synsets(word):
      for i in syn.lemmas():
          name = i.name()
          if '-' in name or '_' in name or name.lower()== word:
            continue
          synonyms.add(i.name())
  return list(synonyms)

def build_pairs(adj, sus, label):
  pairs = set()
  for s in get_syn(sus):
    pairs.add((adj, s, label))
  return pairs

def get_data(path):
  all_data = []
  with open(path, 'r') as file:
    raw_data = file.read().splitlines()
    for d in raw_data:
      data = d.split()
      all_data.append((data[0],data[1], data[2]))
  return all_data

def expand(path):
  data = get_data(path)
  expanded = set()
  for d in data:
    new_data = build_pairs(*d)
    expanded = expanded.union(new_data)
    expanded.add(d)
  return expanded

def save_expanded(data):
    with open('an_joined_expanded.txt', 'w') as f:
        for d in data:
            f.write(' '.join(d)+'\n')