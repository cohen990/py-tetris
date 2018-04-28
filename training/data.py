import numpy


def unison_shuffled_copies(a, b):
    assert len(a) == len(b)
    p = numpy.random.permutation(len(a))
    return a[p], b[p]


def prepare_training_sets(x_batch, y_batch):
    x_batch, y_batch = unison_shuffled_copies(x_batch, y_batch)
    train_length = int(len(x_batch) * 0.8)
    x_train = x_batch[:train_length]
    y_train = y_batch[:train_length]
    x_test = x_batch[train_length:]
    y_test = y_batch[train_length:]
    return x_train, y_train, x_test, y_test
