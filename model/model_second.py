import numpy as np
from tensorflow import keras
from keras.layers import  Input, Dense, GRU
from keras.models import Model
from sklearn.model_selection import  train_test_split
from embeddings import Magnitudes
from corpus import ANCORPUS
from metrics import *

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
KERAS_OPTIMIZER = 'adam'
KERAS_EPOCHS = 10
KERAS_BATCH_SIZE = 40
KERAS_DROPOUT = 0.4
KERAS_ACTIVATION = 'tanh'
KERAS_METRICS = [precision, recall, f1]
loss = keras.losses.CategoricalCrossentropy()
an_input = Input(shape=(2, 300), name='an_input')
model = GRU(100, return_sequences=True, dropout=0, recurrent_dropout=KERAS_DROPOUT,name='hidden_gru')(an_input)
outputs = Dense(1, activation=KERAS_ACTIVATION, name='labels_output')(model)
model = Model(inputs=[an_input], outputs=outputs)
model.compile(optimizer=KERAS_OPTIMIZER,loss= loss, metrics=KERAS_METRICS)
print("Done")
x_train,x_val,y_train,y_val = train_test_split(x_input, y_labels, train_size=0.8)#, shuffle=True,random_state=1337)

# #     # Fit the model for each split
model.fit(x_train, y_train,
            batch_size=KERAS_BATCH_SIZE,
            epochs=KERAS_EPOCHS,)

scores = model.evaluate(x_val, y_val)
print('Loss: {:.2%}'.format(scores[0]))
print('Precision: {:.2%}'.format(scores[1]))
print('Recall: {:.2%}'.format(scores[2]))
print('F1: {:.2%}'.format(scores[3]))

model.save('an_metaphor_gru.h5')
print('Saved model to disk')