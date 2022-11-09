from keras.models import load_model
import keras
import numpy as np
from googletrans import Translator, constants
from metrics import *
from embeddings import Magnitudes
translator = Translator()
model = load_model('an_metaphor_lstm.h5',
                   custom_objects={
                       'loss': keras.losses.CategoricalCrossentropy(),
                       'f1': f1,
                       'precision': precision,
                       'recall': recall
                   })

path = 'model\data\spanish_corpus_translated.txt'
data = []
with open(path, 'r') as file:
  raw_data = file.read().splitlines()
  for d in raw_data:
      dat = d.split()
      if len(dat)==2:
        data.append((dat[0],dat[1]))
embeddings = Magnitudes()
transformed = []
for d in data:
    t = embeddings.embeddings(d)
    transformed.append(t)

x_input = np.array(transformed) 
#probabilidad de no metafora vs probabilidad de metáfora
float_predictions = model.predict(x_input)
labeled_data = []
for i in range(len(float_predictions)):
  prediction = float_predictions[i]
  text = translator.translate(' '.join(data[i]), dest = 'es').text
  label = 1 if prediction[1]> prediction[0] else 0
  labeled_data.append((text, label))
path = 'model\data\spanish_corpus_labeled.txt'
with open(path, 'w+') as file:
  for l in labeled_data:
    file.write(l[0]+ ' '+ str(l[1])+ '\n')