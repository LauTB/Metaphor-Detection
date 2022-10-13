import numpy as np
from tensorflow import keras
from keras.layers import TimeDistributed, Bidirectional, LSTM, Input, Masking, Dense, Lambda
from keras.models import Model
from keras import backend as kerasbackend
from sklearn.model_selection import KFold, train_test_split
from embeddings import Magnitudes
from corpus import ANCORPUS
import tensorflow as tf

def recall(y_true, y_pred):
    """
    Only computes a batch-wise average of recall.
    Computes the recall, a metric for multi-label classification of
    how many relevant items are selected.
    """

    true_positives = kerasbackend.sum(kerasbackend.round(kerasbackend.clip(y_true * y_pred, 0, 1)))
    possible_positives = kerasbackend.sum(kerasbackend.round(kerasbackend.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + kerasbackend.epsilon())

    return recall


def precision(y_true, y_pred):
    """
    Only computes a batch-wise average of precision.
    Computes the precision, a metric for multi-label classification of
    how many selected items are relevant.
    """

    true_positives = kerasbackend.sum(kerasbackend.round(kerasbackend.clip(y_true * y_pred, 0, 1)))
    predicted_positives = kerasbackend.sum(kerasbackend.round(kerasbackend.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + kerasbackend.epsilon())

    return precision


def f1(y_true, y_pred):
    """
    Keras 2.0 doesn't ship the F1 Metric anymore.
    https://github.com/keras-team/keras/issues/6507
    """

    prec = precision(y_true, y_pred)
    reca = recall(y_true, y_pred)

    return 2 * ((prec * reca) / (prec + reca))


KFOLD_SPLIT = 8
KERAS_OPTIMIZER = 'rmsprop'
KERAS_EPOCHS = 5
KERAS_BATCH_SIZE = 32
KERAS_DROPOUT = 0.25
KERAS_ACTIVATION = 'softmax'
KERAS_METRICS = [precision, recall, f1]
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
y_labels = np.array([c for c in corpus.data_lables])
print('Compiling model...')
loss = keras.losses.CategoricalCrossentropy()
an_input = Input(shape=(2, 300), name='an_input')
model = Bidirectional(LSTM(100, return_sequences=True, dropout=0, recurrent_dropout=KERAS_DROPOUT), name='hidden_lstm')(an_input)
outputs = TimeDistributed(Dense(1, activation=KERAS_ACTIVATION), name='labels_output')(model)
#outputs = TimeDistributed(Lambda(lambda x: tf.argmax(x)))(model)
model = Model(inputs=[an_input], outputs=outputs)
model.compile(optimizer=KERAS_OPTIMIZER,loss= loss, metrics=KERAS_METRICS)
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

    scores = model.evaluate([x_val], [y_val])
    print('Loss: {:.2%}'.format(scores[0]))
    print('Precision: {:.2%}'.format(scores[1]))
    print('Recall: {:.2%}'.format(scores[2]))

model.save('an_metaphor.h5')
print('Saved model to disk')