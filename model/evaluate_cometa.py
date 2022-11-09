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