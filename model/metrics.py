from keras import backend as kerasbackend
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