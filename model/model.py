import numpy as np
from tensorflow import keras
from keras.layers import TimeDistributed, Bidirectional, LSTM, Input, Dense
from keras.models import Model
from sklearn.model_selection import  train_test_split
from embeddings import Magnitudes
from corpus import ANCORPUS
from metrics import *

KFOLD_SPLIT = 8
KERAS_OPTIMIZER = 'rmsprop'
KERAS_EPOCHS = 10
KERAS_BATCH_SIZE = 30
KERAS_DROPOUT = 0.3
KERAS_ACTIVATION = 'softmax'
KERAS_METRICS = [precision, recall, f1]
print('Loading embeddings...')
embeddings = Magnitudes()
print('Done')
print('Loading data...')
corpus = ANCORPUS()
corpus.load_data(r'model\data\an_joined_expanded.txt')
print('Done')
print('Applying embeddings...')
transformed_data = corpus.transform_data(embeddings)
print('Done')
print('Deleting embeddings...')
del embeddings
print('Done')
x_input = np.array(transformed_data) 
y_labels = np.array([c for c in corpus.data_lables])
print('Compiling model...')
loss = keras.losses.CategoricalCrossentropy()
an_input = Input(shape=(2, 300), name='an_input')
model = Bidirectional(LSTM(100, return_sequences=True, dropout=0, recurrent_dropout=KERAS_DROPOUT), name='hidden_lstm')(an_input)
outputs = TimeDistributed(Dense(1, activation=KERAS_ACTIVATION), name='labels_output')(model)
model = Model(inputs=[an_input], outputs=outputs)
model.compile(optimizer=KERAS_OPTIMIZER,loss= loss, metrics=KERAS_METRICS)
print('Done')
print(model.summary())

x_train,x_val,y_train,y_val = train_test_split(x_input, y_labels, train_size=0.8)

model.fit(x_train, y_train,
            batch_size=KERAS_BATCH_SIZE,
            epochs=KERAS_EPOCHS,)

scores = model.evaluate([x_val], y_val)
print('Loss: {:.2%}'.format(scores[0]))
print('Precision: {:.2%}'.format(scores[1]))
print('Recall: {:.2%}'.format(scores[2]))
print('F1: {:.2%}'.format(scores[3]))

model.save('an_metaphor_lstm.h5')
print('Saved model to disk')