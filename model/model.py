import numpy as np
from tensorflow import keras
from keras.layers import TimeDistributed, Bidirectional, LSTM, Input, Masking, Dense
from keras.models import Model
from sklearn.model_selection import KFold, train_test_split
from embeddings import Magnitudes
from corpus import ANCORPUS

KFOLD_SPLIT = 8
KERAS_OPTIMIZER = 'rmsprop'
KERAS_EPOCHS = 5
KERAS_BATCH_SIZE = 32
KERAS_DROPOUT = 0.25
KERAS_ACTIVATION = 'softmax'
print('Loading embeddings...')
embeddings = Magnitudes()
print('Done')
print('Loading data...')
corpus = ANCORPUS()
corpus.load_data(r'model\data\an_joined.txt')
print('Done')
print('Applying embeddings...')
transformed_data = corpus.transform_data(embeddings)
print('Done')
print('Deleting embeddings...')
del embeddings
print('Done')
x_input = np.array(transformed_data) 
y_labels = np.array([int(c) for c in corpus.data_lables])
print('Compiling model...')
loss = keras.losses.CategoricalCrossentropy()
an_input = Input(shape=(2, 300), name='an_input')
#model = Masking(mask_value=[-1] * 300, name='masking_padding')(an_input)
model = Bidirectional(LSTM(100, return_sequences=True, dropout=0, recurrent_dropout=KERAS_DROPOUT), name='hidden_lstm')(an_input)
outputs = TimeDistributed(Dense(2, activation=KERAS_ACTIVATION), name='labels_output')(model)
model = Model(inputs=[an_input], outputs=outputs)
model.compile(optimizer=KERAS_OPTIMIZER,loss= loss)
print('Done')
print(model.summary())
kfold = KFold(n_splits=KFOLD_SPLIT, shuffle=True, random_state=1337)
for train, test in kfold.split(x_input, y_labels):
    x_train = x_input[train]
    x_val = x_input[test]
    y_train = y_labels[train]
    y_val = y_labels[test]


#     # Fit the model for each split
    model.fit(x_train, y_train,
              batch_size=KERAS_BATCH_SIZE,
              epochs=KERAS_EPOCHS,)

    scores = model.evaluate([x_val], y_val)
    print('Loss: {:.2%}'.format(scores[0]))
    print('Precision: {:.2%}'.format(scores[1]))
    print('Recall: {:.2%}'.format(scores[2]))

model.save('an_metaphor.h5')
print('Saved model to disk')