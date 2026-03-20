import numpy


def unison_shuffle(arrays):
    p = numpy.random.permutation(len(arrays[0]))
    return [a[p] for a in arrays]


def prepare_training_sets(boards, contexts, y_batch):
    boards, contexts, y_batch = unison_shuffle([boards, contexts, y_batch])
    train_length = int(len(boards) * 0.8)
    return (boards[:train_length], contexts[:train_length], y_batch[:train_length],
            boards[train_length:], contexts[train_length:], y_batch[train_length:])
